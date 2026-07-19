import { readFile, stat } from "node:fs/promises";

const registry = JSON.parse(await readFile("data/customer-contracts.json", "utf8"));
const runtime = await readFile("scripts/build_level_viewer_v4.py", "utf8");
if (registry.customers.length < 4) throw new Error("At least four launch customers are required.");
const ids = new Set(), offers = new Set();
for (const customer of registry.customers) {
  if (ids.has(customer.id)) throw new Error(`Duplicate customer: ${customer.id}`);
  ids.add(customer.id);
  if (!customer.contact || !customer.title || !customer.company || !customer.industry || !customer.description) throw new Error(`Incomplete customer profile: ${customer.id}`);
  const offer = customer.offer;
  if (!offer?.id || offers.has(offer.id) || !["drill", "pocket", "dome"].includes(offer.jobFamily)) throw new Error(`Invalid offer: ${customer.id}`);
  offers.add(offer.id);
  if (!(offer.quantity > 0 && offer.unitPrice > 0 && offer.dueShifts > 0 && offer.requirements?.length >= 3)) throw new Error(`Incomplete contract terms: ${offer.id}`);
}
for (const asset of ["customer-profiles-v1.png", "customer-sprites-v1.png", "customer-companies-v1.png", "shop-communications-v1.png"]) {
  const info = await stat(`packages/assets/customers/${asset}`);
  if (info.size < 10_000) throw new Error(`Customer art invalid: ${asset}`);
}
for (const token of ["SHOP PHONE", "JOBLINE MAIL", "acceptCustomerContract", "pendingContract", "released to production", "state.reputation"]) {
  if (!runtime.includes(token)) throw new Error(`Customer runtime hook missing: ${token}`);
}
console.log(`PASS: ${registry.customers.length} customer profiles, companies, RFQs, channels, art atlases, and JobLine handoff hooks verified.`);
