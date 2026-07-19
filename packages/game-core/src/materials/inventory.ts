/** NOX Metals ordering + stock. Delivery arrives as a sim event after leadTicks. */
import type { GameState, Tick } from "../types";

export interface CatalogItem {
  sku: string; name: string; family: string; basePrice: number;
  leadTicks: number; machinability: number; sfm: { carbide: number };
  certRequired?: boolean; unlocksAtTier?: number;
}
export interface StockLine { sku: string; qty: number; certed: boolean }
export interface PendingOrder { sku: string; qty: number; certed: boolean; arrivesAt: Tick; rush: boolean }

export function orderCost(item: CatalogItem, qty: number, opts: { cert: boolean; rush: boolean }, priceDrift = 1) {
  let unit = item.basePrice * priceDrift;
  if (opts.cert) unit *= 1.1;
  if (opts.rush) unit *= 1.5;
  return Math.round(unit * qty);
}

export function placeOrder(
  s: GameState & { stock?: StockLine[]; pendingOrders?: PendingOrder[] },
  item: CatalogItem, qty: number, opts: { cert: boolean; rush: boolean }, priceDrift = 1
): { ok: boolean; reason?: string } {
  const cost = orderCost(item, qty, opts, priceDrift);
  if (s.player.coins < cost) return { ok: false, reason: "insufficient_coins" };
  if (item.unlocksAtTier && s.player.tier < item.unlocksAtTier) return { ok: false, reason: "tier_locked" };
  s.player.coins -= cost;
  (s.pendingOrders ??= []).push({
    sku: item.sku, qty, certed: opts.cert, rush: opts.rush,
    arrivesAt: s.tick + Math.round(item.leadTicks * (opts.rush ? 0.5 : 1)),
  });
  s.eventLog.push({ t: s.tick, type: "material.ordered", data: { sku: item.sku, qty, vendor: "vendor_nox" } });
  return { ok: true };
}

/** Called each tick from sim.step(): deliver arrived orders to receiving. */
export function processDeliveries(s: GameState & { stock?: StockLine[]; pendingOrders?: PendingOrder[] }) {
  if (!s.pendingOrders?.length) return;
  const arrived = s.pendingOrders.filter(o => o.arrivesAt <= s.tick);
  s.pendingOrders = s.pendingOrders.filter(o => o.arrivesAt > s.tick);
  for (const o of arrived) {
    const line = (s.stock ??= []).find(l => l.sku === o.sku && l.certed === o.certed);
    if (line) line.qty += o.qty; else s.stock.push({ sku: o.sku, qty: o.qty, certed: o.certed });
    s.eventLog.push({ t: s.tick, type: "material.received", data: { sku: o.sku, qty: o.qty, certed: o.certed } });
  }
}
