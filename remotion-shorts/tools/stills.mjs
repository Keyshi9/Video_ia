// usage: node tools/stills.mjs <outPrefix> <frame,frame,...> [scale]
// env: ENTRY (default src/index.tsx; a sandbox: src/sandboxes/<n>/index.tsx), COMP (default Bastille)
// One render at a time on this PC (16 GB RAM, integrated GPU): a lock folder queues concurrent callers.
import fs from "node:fs";
import path from "node:path";
process.env.REMOTION_TMP ||= "C:/Users/pu99cle/remotion-tmp";
fs.mkdirSync(process.env.REMOTION_TMP, { recursive: true });
process.env.TEMP = process.env.TMP = process.env.REMOTION_TMP;
const { bundle } = await import("@remotion/bundler");
const { renderStill, selectComposition } = await import("@remotion/renderer");

const LOCK = "C:/Users/pu99cle/remotion-tmp/render.lock";
const sleep = (ms) => new Promise((r) => setTimeout(r, ms));
const lock = async () => {
  for (;;) {
    try { fs.mkdirSync(LOCK); fs.writeFileSync(LOCK + "/pid", String(process.pid)); return; }
    catch {
      try { if (Date.now() - fs.statSync(LOCK).mtimeMs > 12 * 60e3) fs.rmSync(LOCK, { recursive: true, force: true }); } catch {}
      await sleep(2000);
    }
  }
};
const unlock = () => fs.rmSync(LOCK, { recursive: true, force: true });
process.on("exit", unlock); process.on("SIGINT", () => process.exit(1));

const [prefix, frames, scale = "0.5"] = process.argv.slice(2);
fs.mkdirSync(path.dirname(prefix), { recursive: true });
const browserExecutable = "C:/Program Files/Google/Chrome/Application/chrome.exe";
const chromiumOptions = { gl: "angle" };
await lock();
const serveUrl = await bundle({ entryPoint: path.resolve(process.env.ENTRY || "src/index.tsx"), publicDir: path.resolve("public") });
const composition = await selectComposition({ serveUrl, id: process.env.COMP || "Bastille", browserExecutable, chromiumOptions });
const onBrowserLog = (l) => { if ((l.type === "error" || l.type === "warning") && !l.text.includes("404")) console.log(`[${l.type}]`, l.text.slice(0, 300)); };
for (const f of frames.split(",").map(Number)) {
  const t0 = Date.now();
  await renderStill({ composition, serveUrl, frame: f, output: `${prefix}${f}.jpg`, imageFormat: "jpeg", jpegQuality: 88, scale: Number(scale),
    browserExecutable, chromiumOptions, timeoutInMilliseconds: 180000, onBrowserLog });
  console.log("still", f, ((Date.now() - t0) / 1000).toFixed(1) + "s");
}
unlock();
