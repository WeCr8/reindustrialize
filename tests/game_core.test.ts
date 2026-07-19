import assert from "node:assert/strict";
import test from "node:test";
import {checkAnswers, createGame, dispatch, feedFor, migrateSave, orderCost, placeOrder, QuestEngine, rng, rpmFor, serialize, deserialize, step} from "@wecr8/game-core";

test("deterministic simulation produces identical random streams", () => {
  const a = rng(1987), b = rng(1987);
  assert.deepEqual(Array.from({length: 20}, () => a()), Array.from({length: 20}, () => b()));
});

test("new games satisfy the complete player contract", () => {
  const game = createGame(42, "arcade");
  assert.equal(game.player.avatarId, "av_m_01");
  assert.equal(game.eventLog.length, 0);
  assert.equal(step(game, new QuestEngine([])).tick, 1);
});

test("quest dispatch is logged and rewards only after matching steps", () => {
  const quest = {id:"q1",type:"tutorial",tier:1,lesson:"prove it",steps:[{event:"machine.started"}],rewards:{coins:125,xp:10},zachIntro:[],zachOutro:[]};
  const game = createGame(5, "arcade");
  game.activeQuests = ["q1"];
  const engine = new QuestEngine([quest]);
  dispatch(game, engine, "machine.started", {machine:"vmc"});
  assert.equal(game.player.coins, 625);
  assert.deepEqual(game.completedQuests, ["q1"]);
  assert.equal(game.eventLog.at(-1)?.type, "quest.completed");
});

test("versioned save round-trips and rejects unsupported versions", () => {
  const game = createGame(8, "shop");
  const restored = deserialize(serialize(game));
  assert.deepEqual(restored, game);
  assert.throws(() => deserialize('{"v":999,"state":{}}'), /needs migration/);
});

test("save loading rejects malformed JSON and corrupt state boundaries", () => {
  assert.throws(() => deserialize("not json"), /not valid JSON/);
  assert.throws(() => deserialize('{"v":1}'), /missing its version or state/);
  const game = createGame(8, "shop");
  assert.throws(() => deserialize(JSON.stringify({v:1,state:{...game,tick:-1}})), /corrupt at tick/);
  assert.throws(() => deserialize(JSON.stringify({v:1,state:{...game,player:{...game.player,reputation:101}}})), /player.reputation/);
  assert.throws(() => deserialize(JSON.stringify({v:1,state:{...game,activeQuests:["q1"],completedQuests:["q1"]}})), /activeQuests/);
  assert.throws(() => deserialize(JSON.stringify({v:1,state:{...game,jobs:[{id:"j",part:"p",qty:1,done:2,scrapped:0,route:[],payout:1,dueTick:1,status:"wip"}]}})), /jobs.0/);
});

test("legacy migration is explicit and still schema validated", () => {
  const game = createGame(17, "arcade");
  assert.deepEqual(deserialize(JSON.stringify({v:0,state:game})), game);
  assert.deepEqual(migrateSave({v:0,state:game}), {v:1,state:game});
  assert.throws(() => deserialize('{"v":0,"state":{}}'), /corrupt/);
});

test("quest completion is idempotent for duplicate active ids and replayed events", () => {
  const quest = {id:"q1",type:"tutorial",tier:1,lesson:"prove it",steps:[{event:"machine.started"}],rewards:{coins:125,xp:10},zachIntro:[],zachOutro:[]};
  const game = createGame(5, "arcade");
  game.activeQuests = ["q1", "q1"];
  const engine = new QuestEngine([quest]);
  dispatch(game, engine, "machine.started");
  dispatch(game, engine, "machine.started");
  assert.equal(game.player.coins, 625);
  assert.deepEqual(game.completedQuests, ["q1"]);
  assert.equal(game.eventLog.filter(event => event.type === "quest.completed").length, 1);
});

test("material orders are priced, gated, and logged", () => {
  const game = createGame(9, "arcade");
  const item = {sku:"AL6061",name:"6061",family:"aluminum",basePrice:100,leadTicks:5,machinability:0.9,sfm:{carbide:600}};
  assert.equal(orderCost(item, 2, {cert:true,rush:false}), 220);
  assert.equal(placeOrder(game, item, 2, {cert:true,rush:false}).ok, true);
  assert.equal(game.player.coins, 280);
  assert.equal(game.eventLog.at(-1)?.type, "material.ordered");
});

test("material ordering rejects invalid quantities and certification violations without mutation", () => {
  const game = createGame(9, "arcade");
  const item = {sku:"SS316",name:"316",family:"steel",basePrice:100,leadTicks:5,machinability:0.5,sfm:{carbide:300},certRequired:true};
  const coins = game.player.coins;
  assert.deepEqual(placeOrder(game, item, 0, {cert:true,rush:false}), {ok:false,reason:"invalid_quantity"});
  assert.deepEqual(placeOrder(game, item, 1, {cert:false,rush:false}), {ok:false,reason:"cert_required"});
  assert.equal(game.player.coins, coins);
  assert.equal(game.eventLog.length, 0);
  assert.throws(() => orderCost(item, 1.5, {cert:true,rush:false}), /positive integer/);
  assert.throws(() => orderCost(item, 1, {cert:true,rush:false}, Number.NaN), /price drift/);
});

test("G-code calculations and validation use the active material", () => {
  const material = {sfm:600,machinability:0.9};
  const rpm = rpmFor(material, 0.5), feed = feedFor(rpm, 4, 0.002);
  assert.ok(rpm > 4500 && feed > 35);
  const def = {id:"g1",tier:1,machineClass:"vmc",lesson:"feeds",context:{toolDia:0.5,flutes:4,chipLoad:0.002},program:[],blanks:{rpm:{validate:"range" as const,compute:"rpmFromMaterial" as const,tolerance:0.05,hint:"check rpm"}},zachFail:[],zachPass:[]};
  assert.equal(checkAnswers(def, material, {rpm:String(Math.round(rpm))}).pass, true);
  assert.equal(checkAnswers(def, material, {rpm:"100"}).pass, false);
});
