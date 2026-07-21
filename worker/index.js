import QRCode from "qrcode";

const controllerHtml = token => `<!doctype html><html><head><meta name="viewport" content="width=device-width,initial-scale=1,maximum-scale=1,user-scalable=no"><title>REINDUSTRIALIZE Phone Controller</title><style>*{box-sizing:border-box;touch-action:none}body{margin:0;min-height:100dvh;display:grid;place-items:center;background:#080b10;color:#fff;font:18px monospace}.wrap{text-align:center;width:min(520px,96vw)}#status{color:#3fd08a}.pad{display:grid;grid-template-columns:repeat(3,88px);gap:9px;justify-content:center}.b{height:78px;border:3px solid #e8b93b;border-radius:9px;background:#111820;color:#e8b93b;font-size:30px}.b.on{background:#e8b93b;color:#080b10}.x{visibility:hidden}.menu{margin-top:18px;width:184px;border-color:#3fd08a;color:#3fd08a}</style></head><body><main class="wrap"><h1>SHOP CONTROLLER</h1><p id="status">PAIRING…</p><div class="pad"><i></i><button class="b" data-key="up">▲</button><i></i><button class="b" data-key="left">◀</button><button class="b" data-key="action">●</button><button class="b" data-key="right">▶</button><i></i><button class="b" data-key="down">▼</button><i></i></div><button class="b menu" data-key="menu">MENU</button></main><script>const token=${JSON.stringify(token)},status=document.querySelector('#status'),ws=new WebSocket('wss://'+location.host+'/pair?token='+encodeURIComponent(token)+'&role=controller');ws.onopen=()=>status.textContent='CONNECTED';ws.onclose=()=>status.textContent='DISCONNECTED';const send=(key,state)=>ws.readyState===1&&ws.send(JSON.stringify({type:'input',key,state}));document.querySelectorAll('[data-key]').forEach(b=>{const done=e=>{e.preventDefault();b.classList.remove('on');send(b.dataset.key,false)};b.onpointerdown=e=>{e.preventDefault();b.setPointerCapture(e.pointerId);b.classList.add('on');send(b.dataset.key,true);navigator.vibrate?.(18)};b.onpointerup=done;b.onpointercancel=done});</script></body></html>`;

export class ControllerSession {
  constructor(state) { this.state=state; }
  async fetch(request) {
    const url=new URL(request.url);
    if(url.pathname==="/init"){await this.state.storage.put("valid",true);return new Response("ok");}
    if(!(await this.state.storage.get("valid"))||(request.headers.get("Upgrade")||"").toLowerCase()!=="websocket")return new Response("Invalid session",{status:403});
    const role=url.searchParams.get("role");if(!["host","controller"].includes(role))return new Response("Invalid role",{status:400});
    if(this.state.getWebSockets(role).length)return new Response("Role already connected",{status:409});
    const pair=new WebSocketPair(),client=pair[0],server=pair[1];server.serializeAttachment({role});this.state.acceptWebSocket(server,[role]);this.notify();
    return new Response(null,{status:101,webSocket:client});
  }
  notify(){const host=this.state.getWebSockets("host")[0];if(host)try{host.send(JSON.stringify({type:"status",connected:this.state.getWebSockets("controller").length>0}))}catch{}}
  webSocketMessage(socket,data){const role=socket.deserializeAttachment()?.role;if(role!=="controller")return;try{const m=JSON.parse(data);if(m.type!=="input"||!["up","down","left","right","action","menu","run"].includes(m.key)||typeof m.state!=="boolean")return;this.state.getWebSockets("host")[0]?.send(JSON.stringify(m));}catch{}}
  webSocketClose(){this.notify()}
  webSocketError(){this.notify()}
}

export default {async fetch(request,env){
  const url=new URL(request.url);
  if(url.pathname==="/api/controller-session"&&request.method==="POST"){
    const token=[...crypto.getRandomValues(new Uint8Array(16))].map(x=>x.toString(16).padStart(2,"0")).join("");
    const stub=env.CONTROLLER_SESSIONS.get(env.CONTROLLER_SESSIONS.idFromName(token));await stub.fetch("https://session/init");
    const controllerUrl=`${url.origin}/controller?token=${token}`,svg=await QRCode.toString(controllerUrl,{type:"svg",margin:1,width:256});
    return Response.json({token,controllerUrl,qr:`data:image/svg+xml;base64,${btoa(unescape(encodeURIComponent(svg)))}`},{headers:{"cache-control":"no-store"}});
  }
  if(url.pathname==="/controller"){
    const token=url.searchParams.get("token")||"";if(!/^[a-f0-9]{32}$/.test(token))return new Response("Invalid pairing code",{status:400});
    return new Response(controllerHtml(token),{headers:{"content-type":"text/html;charset=UTF-8","cache-control":"no-store"}});
  }
  if(url.pathname==="/pair"){
    const token=url.searchParams.get("token")||"";if(!/^[a-f0-9]{32}$/.test(token))return new Response("Invalid pairing code",{status:400});
    return env.CONTROLLER_SESSIONS.get(env.CONTROLLER_SESSIONS.idFromName(token)).fetch(request);
  }
  return env.ASSETS.fetch(request);
}};
