import { createHash } from "node:crypto";
import { mkdir, readFile, rename, writeFile } from "node:fs/promises";
import { dirname, join, resolve } from "node:path";
import { fileURLToPath } from "node:url";

const root = resolve(dirname(fileURLToPath(import.meta.url)), "..");
const manifestPath = join(root, "data", "audio-generation.json");
const outputRoot = join(root, "packages", "assets", "audio", "generated");
const dryRun = process.argv.includes("--dry-run");
const voiceOnly = process.argv.includes("--voice-only");
const musicOnly = process.argv.includes("--music-only");
const sfxOnly = process.argv.includes("--sfx-only");
const idsArg = process.argv.find(x => x.startsWith("--ids="));
const requestedIds = idsArg ? new Set(idsArg.slice(6).split(",").map(x => x.trim()).filter(Boolean)) : null;
if ([voiceOnly, musicOnly, sfxOnly].filter(Boolean).length > 1) throw new Error("Choose only one of --voice-only, --music-only, or --sfx-only.");

const config = JSON.parse(await readFile(manifestPath, "utf8"));
let selected = [
  ...(!musicOnly && !sfxOnly ? config.voice.clips.map(x => ({ kind: "voice", ...x })) : []),
  ...(!voiceOnly && !sfxOnly ? config.music.tracks.map(x => ({ kind: "music", ...x })) : []),
  ...(!voiceOnly && !musicOnly ? config.sfx.effects.map(x => ({ kind: "sfx", ...x })) : []),
];
if (requestedIds) {
  selected = selected.filter(item => requestedIds.has(item.id));
  const missing = [...requestedIds].filter(id => !selected.some(item => item.id === id));
  if (missing.length) throw new Error(`Unknown or excluded audio IDs: ${missing.join(", ")}`);
}
console.log(`${dryRun ? "PLAN" : "GENERATE"}: ${selected.length} assets (${selected.filter(x => x.kind === "voice").length} voice, ${selected.filter(x => x.kind === "music").length} music, ${selected.filter(x => x.kind === "sfx").length} sfx)`);
for (const item of selected) console.log(`- ${item.kind}: ${item.id}`);
if (dryRun) process.exit(0);

const apiKey = process.env.ELEVENLABS_API_KEY;
const voiceId = process.env.ELEVENLABS_ZACH_VOICE_ID;
const consent = process.env.ZACH_VOICE_CONSENT_CONFIRMED === "yes";
const apiBase = (process.env.ELEVENLABS_API_BASE || "https://api.elevenlabs.io").replace(/\/$/, "");
if (!apiKey) throw new Error("ELEVENLABS_API_KEY is required. Keep it in the environment; never put it in browser code.");
if ([".env", "your-key", "your_api_key", "changeme"].includes(apiKey.trim().toLowerCase())) throw new Error("ELEVENLABS_API_KEY is still a placeholder. Put the real key in the ignored .env file; do not set the key to the filename.");
if (!musicOnly && !sfxOnly && (!voiceId || !consent)) throw new Error("Zach voice generation requires ELEVENLABS_ZACH_VOICE_ID and ZACH_VOICE_CONSENT_CONFIRMED=yes.");
if (!apiBase.startsWith("https://")) throw new Error("ELEVENLABS_API_BASE must use HTTPS.");

async function requestAudio(url, body) {
  const response = await fetch(url, {
    method: "POST",
    headers: { "xi-api-key": apiKey, "content-type": "application/json", accept: "audio/mpeg" },
    body: JSON.stringify(body),
    signal: AbortSignal.timeout(600_000),
  });
  if (!response.ok) {
    const message = (await response.text()).slice(0, 500);
    throw new Error(`ElevenLabs returned ${response.status}: ${message}`);
  }
  return { bytes: Buffer.from(await response.arrayBuffer()), requestId: response.headers.get("request-id") };
}

async function saveAtomic(kind, id, result, requestBody) {
  const directory = join(outputRoot, kind);
  await mkdir(directory, { recursive: true });
  const target = join(directory, `${id}.mp3`);
  const temp = `${target}.partial`;
  await writeFile(temp, result.bytes, { mode: 0o600 });
  await rename(temp, target);
  const receipt = {
    id, kind, generatedAt: new Date().toISOString(), requestId: result.requestId,
    sha256: createHash("sha256").update(result.bytes).digest("hex"),
    request: { ...requestBody, text: requestBody.text ? "[stored in data/audio-generation.json]" : undefined },
  };
  await writeFile(join(directory, `${id}.receipt.json`), `${JSON.stringify(receipt, null, 2)}\n`, { mode: 0o600 });
  console.log(`wrote ${kind}/${id}.mp3`);
}

for (const item of selected) {
  if (item.kind === "voice") {
    const selectedVoiceId = item.role === "player" ? item.voiceId : voiceId;
    if (!selectedVoiceId) throw new Error(`No voice ID configured for ${item.id}.`);
    const body = { text: item.text, model_id: item.modelId || config.voice.modelId, ...(item.voiceSettings ? {voice_settings:item.voiceSettings} : {}) };
    const url = `${apiBase}/v1/text-to-speech/${encodeURIComponent(selectedVoiceId)}?output_format=${encodeURIComponent(config.voice.outputFormat)}&enable_logging=${config.voice.enableLogging}`;
    await saveAtomic("voice", item.id, await requestAudio(url, body), body);
  } else if (item.kind === "music") {
    const body = { prompt: item.prompt, music_length_ms: item.lengthMs, model_id: config.music.modelId, force_instrumental: true, store_for_inpainting: false, sign_with_c2pa: config.music.signWithC2pa };
    const url = `${apiBase}/v1/music?output_format=${encodeURIComponent(config.music.outputFormat)}`;
    await saveAtomic("music", item.id, await requestAudio(url, body), body);
  } else {
    const body = { text: item.prompt, duration_seconds: item.durationSeconds, loop: item.loop, prompt_influence: config.sfx.promptInfluence, model_id: config.sfx.modelId };
    const url = `${apiBase}/v1/sound-generation?output_format=${encodeURIComponent(config.sfx.outputFormat)}`;
    await saveAtomic("sfx", item.id, await requestAudio(url, body), body);
  }
}
