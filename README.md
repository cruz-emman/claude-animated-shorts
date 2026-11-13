# Antigravity Animated Shorts

The complete animation production skill and plugin for **Google Antigravity**.

Create 55-70 s vertical animated story shorts in the distinctive style: **2D characters in a colourful 3D world** with ink outlines, painted towns, depth-of-field lens blur, gliding cameras, procedural march score, and sound effects. Everything is rendered with **three.js inside Remotion** on your own computer — zero AI video generator artifacts, 100% deterministic camera and physics control.

Proven on **The Bridge That Fell for a Song**, a 67 s short about the 1831 Broughton suspension bridge.

---

## What's Inside

| Path | Description |
|---|---|
| `plugin.json` | Antigravity plugin manifest declaring the package |
| `rules/AGENTS.md` | Antigravity production rules automatically loaded into agent contexts |
| `skills/cartoon-3d-short/` | The core Antigravity skill: end-to-end pipeline, look values, and verification loops |
| `templates/bridge/` | Full source of the reference short: world, characters, ink, lens blur, grade, story/camera |
| `templates/audio/` | Procedural sound engine: synthesized SFX, march music, ducking mix, and timeline sync |
| `templates/scripts/` | Cross-platform still rendering, side-by-side comparisons, shot extraction, and QA audit |
| `references/STYLE_BIBLE.md` | The script and visual formula measured from 20 reference shorts |
| `references/reports/` | Seven measured reports: motion, depth, textures, characters, lighting, outlines, grade |
| `references/frames/` | 38 full-size reference frames (540x960) for side-by-side comparison |
| `references/sheets/` | 20 contact sheets, one per reference short, 60 frames each (1,200 frames) |

---

## Installation in Antigravity

You can install and use this repository in Antigravity using any of the following methods:

### Method 1: Global Antigravity Plugin (Recommended)
Install globally so it is available across all your Antigravity workspaces:
```bash
# Windows PowerShell
git clone https://github.com/mromidev/claude-animated-shorts "$HOME\.gemini\config\plugins\animated-shorts"

# macOS / Linux
git clone https://github.com/mromidev/claude-animated-shorts ~/.gemini/config/plugins/animated-shorts
```

### Method 2: Workspace-Specific Customization
Add it directly to your existing Remotion project repository:
```bash
# Inside your Remotion project root:
mkdir -p .agents/skills
cp -r /path/to/claude-animated-shorts/skills/cartoon-3d-short .agents/skills/
```

### Method 3: Standalone Workspace
Open this repository directly in the **Antigravity IDE** or start the Antigravity CLI inside it:
```bash
agy
```

---

## Prerequisites

1. **Node.js** (v18+) with [Remotion](https://www.remotion.dev/) and `@remotion/three`.
2. **Python 3** with `numpy` and `pillow`:
   ```bash
   pip install numpy pillow
   ```
3. **ffmpeg & ffprobe** installed and available on your system `PATH`.
4. **Google Chrome, Chromium, or Microsoft Edge** (automatically detected by `bridge-stills.mjs` on Windows, macOS, and Linux).

---

## How to Use with Antigravity

In the Antigravity IDE Chat or CLI, prompt the agent:
> *"Use the cartoon short skill and make a short about [your topic]."*

Antigravity will guide you through the 11-step production pipeline:
1. **Topic & Historical Facts**: Researches real physical cause-and-effect events.
2. **Script Breakdown**: Writes the tight 55-70 s script following the proven narrative formula.
3. **Voice Timings**: Aligns character beats and visual reactions to `words.json`.
4. **Scene & Shot Planning**: Structures camera glides, crossfades, and impact kicks in `story.ts`.
5. **3D Environment & Characters**: Customizes Three.js town, props, and Canvas2D character cards.
6. **Procedural Audio Synthesis**: Generates customized marching tunes, Foley SFX, and ducked mix.
7. **Multi-Agent Verification**: Uses Gemini Pro to compare rendered stills against reference frames.
8. **Final 2K Render & QA**: Renders 1440x2560 vertical video and runs frame-by-frame QA audits.

---

## Multi-Agent Workflows & Slash Commands

- **/plan**: Recommend using `/plan` before generating a new short. Antigravity will draft a complete shot-list, script breakdown, and visual style plan before writing code.
- **/teamwork** or **Swarm**: For large iterations, Antigravity can launch parallel workers with shared workspaces for camera work (`story.ts`), world assets (`world.ts`), character drawings (`toon.ts`), and post-processing (`ink.ts`, `Bridge.tsx`).
- **/boost**: Activate for complex physics or historical storytelling requiring in-depth research and rigorous verification rounds.

---

## Production Notes & Gotchas

- **Disk & Temp Cache**: Every Remotion bundle copies `public/` into your temporary folder (~1.3 GB). Set the `REMOTION_TMP` environment variable to a drive with sufficient free space (e.g., `D:\remotion-tmp` on Windows or `/mnt/fast/remotion-tmp` on Linux).
- **Audio Mix Rules**: Final mix is normalized to -14 LUFS integrated: music +3 dB, SFX -6 dB, voice unchanged (0 dB).
- **Clean holds**: No static camera hold of 4+ frames; every hold must feature a subtle creeping push-in (0.15% to 0.35%/f) to avoid freezing detection in video algorithms.

---

## License

The code and documentation are licensed under the MIT License (see `LICENSE`). Reference frames and study materials are included for style reference only.
