// usage: node scripts/bridge-stills.mjs <outPrefix> <frame,frame,...> [scale]
// Environment variables:
//   BRIDGE_ENTRY: Entrypoint file (defaults to "src/index.ts")
//   REMOTION_TMP: Temp directory for bundles (defaults to system temp)
//   REMOTION_COMPOSITION: Composition ID (defaults to "BridgeShort")
//   CHROME_PATH / PUPPETEER_EXECUTABLE_PATH: Optional browser path override
import fs from "node:fs";
import path from "node:path";
import os from "node:os";

// Each bundle copies public/ into the temp directory (~1.3 GB).
// Use REMOTION_TMP if defined to redirect to a drive with ample space.
if (process.env.REMOTION_TMP) {
  try {
    fs.mkdirSync(process.env.REMOTION_TMP, { recursive: true });
    process.env.TEMP = process.env.TMP = process.env.REMOTION_TMP;
  } catch (err) {
    console.warn(`[WARN] Could not create REMOTION_TMP directory: ${err.message}`);
  }
}

import { bundle } from "@remotion/bundler";
import { renderStill, selectComposition } from "@remotion/renderer";

function resolveBrowserExecutable() {
  if (process.env.PUPPETEER_EXECUTABLE_PATH && fs.existsSync(process.env.PUPPETEER_EXECUTABLE_PATH)) {
    return process.env.PUPPETEER_EXECUTABLE_PATH;
  }
  if (process.env.CHROME_PATH && fs.existsSync(process.env.CHROME_PATH)) {
    return process.env.CHROME_PATH;
  }

  const platform = os.platform();
  const candidates = [];

  if (platform === "win32") {
    const progFiles = process.env["ProgramFiles"] || "C:\\Program Files";
    const progFilesX86 = process.env["ProgramFiles(x86)"] || "C:\\Program Files (x86)";
    const localAppData = process.env["LOCALAPPDATA"] || "";
    candidates.push(
      path.join(progFiles, "Google", "Chrome", "Application", "chrome.exe"),
      path.join(progFilesX86, "Google", "Chrome", "Application", "chrome.exe"),
      localAppData ? path.join(localAppData, "Google", "Chrome", "Application", "chrome.exe") : null,
      path.join(progFilesX86, "Microsoft", "Edge", "Application", "msedge.exe"),
      path.join(progFiles, "Microsoft", "Edge", "Application", "msedge.exe")
    );
  } else if (platform === "darwin") {
    candidates.push(
      "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
      "/Applications/Chromium.app/Contents/MacOS/Chromium",
      "/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge"
    );
  } else {
    candidates.push(
      "/usr/bin/google-chrome",
      "/usr/bin/google-chrome-stable",
      "/usr/bin/chromium",
      "/usr/bin/chromium-browser"
    );
  }

  for (const c of candidates) {
    if (c && fs.existsSync(c)) {
      return c;
    }
  }
  return undefined; // Let Remotion / Puppeteer find the default system browser
}

const [prefix, framesArg, scale = "0.5"] = process.argv.slice(2);
if (!prefix || !framesArg) {
  console.error("Usage: node scripts/bridge-stills.mjs <outPrefix> <frame,frame,...> [scale]");
  process.exit(1);
}

const browserExecutable = resolveBrowserExecutable();
if (browserExecutable) {
  console.log(`[STILLS] Using browser: ${browserExecutable}`);
}
const chromiumOptions = { gl: "angle" };

const entryPoint = path.resolve(process.env.BRIDGE_ENTRY || "src/index.ts");
const publicDir = path.resolve("public");
const compositionId = process.env.REMOTION_COMPOSITION || "BridgeShort";

console.log(`[STILLS] Bundling composition "${compositionId}" from ${entryPoint}...`);
const serveUrl = await bundle({ entryPoint, publicDir });

const composition = await selectComposition({
  serveUrl,
  id: compositionId,
  ...(browserExecutable ? { browserExecutable } : {}),
  chromiumOptions
});

const onBrowserLog = (l) => {
  if (l.type === "error" || l.type === "warning") {
    console.log(`[${l.type}]`, l.text.slice(0, 300));
  }
};

const frames = framesArg.split(",").map((s) => Number.parseInt(s.trim(), 10)).filter((n) => !Number.isNaN(n));
console.log(`[STILLS] Rendering ${frames.length} frames at scale ${scale}...`);

for (const f of frames) {
  const t0 = Date.now();
  const outputPath = `${prefix}${f}.jpg`;
  const outputDir = path.dirname(path.resolve(outputPath));
  if (!fs.existsSync(outputDir)) {
    fs.mkdirSync(outputDir, { recursive: true });
  }

  await renderStill({
    composition,
    serveUrl,
    frame: f,
    output: outputPath,
    imageFormat: "jpeg",
    jpegQuality: 88,
    scale: Number(scale),
    ...(browserExecutable ? { browserExecutable } : {}),
    chromiumOptions,
    timeoutInMilliseconds: 180000,
    onBrowserLog
  });
  console.log(`still ${f}: ${((Date.now() - t0) / 1000).toFixed(1)}s -> ${outputPath}`);
}
