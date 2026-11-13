---
name: cartoon-3d-short
description: Make a ~55-70 s vertical cartoon story short in the "2D characters in a colourful 3D world" style (flat bean-head cartoon cards with ink outlines, painted 3D town/world with black ink lines, saturated sky, depth-of-field backgrounds, gliding cameras, voice narration, synthesized SFX + march-style music), rendered with three.js inside Remotion. Proven on "The Bridge That Fell for a Song" (2026-10-31). Use when the user asks for another video "like the bridge video", "like the soldiers/bridge short", "in that cartoon 3D style", a history/science story short with cartoon characters in 3D, or says "use the cartoon short skill".
---

# Cartoon 3D story short (three.js + Remotion)

Proven example: **The Bridge That Fell for a Song**. It is an original 67 s short about the 1831 Broughton bridge and 74 soldiers marching in step.
- Code: `src/videos/bridge/` of your Remotion project (composition `BridgeShort`, 1080x1920, 30 fps).
- Script, voice and sound: `~/bridge-short/` or `<project-dir>/audio/`.
- Style research: `references/`.

The style reference is a channel studied privately (`references/`: `STYLE_BIBLE.md`, `reports/*.md`, `frames/`).
- Those videos are private study material. Never upload, publish or send them.
- Never copy their scripts, characters or shots. Story, characters and voice are always OUR OWN.
- Never say the reference channel's name in a voice-over or description.

Production rules that apply:
- No captions or labels in the video.
- English only.
- Voice: one steady narrator tone.
- Jokes are researched real facts.
- Standard mix: music +3 dB, SFX -6 dB, voice unchanged (-14 LUFS integrated).
- Final export 2K vertical: 1440x2560, `--scale 1.3333`.
- Gemini Pro verification audits verify every check.
- Save work and plan state after every step.
- "Just do it" once the script and shot plan are approved.

## Antigravity Multi-Agent Pipeline

1. **Topic and facts.** Pick one surprising true story with a physical cause and effect (it should be visual), plus a simple everyday analogy that explains it.
   - Write the facts with their source at the top of `SCRIPT.md`.
2. **Script** (~3.7 words/s, 55-70 s). Beat formula from the bridge short:
   - **Hook:** the absurd fact in one line ("Seventy-four soldiers knocked down an iron bridge just by walking across it.").
   - **Setting:** year, place, pride.
   - **Action:** escalation over three or four beats, each a little bigger.
   - **Snap:** the moment it breaks.
   - **Deadpan double line:** "Luckily ... / Unluckily ...".
   - **Explanation:** one physics idea through an everyday analogy (the kid on a swing).
   - **Consequence:** the rule it created.
   - **Callback twist:** the ending punchline.
   - Never describe on screen what the viewer already sees.
3. **Voice.** Record or generate `voice.wav`, then make its word timings `words.json` (any speech-to-text with word times).
   - Put them in the project folder, e.g. `voice/words.json`.
   - Hand-fix the word timings. Everything in the animation is timed to `words.json`.
4. **Shot plan** in `story.ts`: copy `templates/bridge/` (the final bridge source, same as `src/videos/bridge/` of your Remotion project) to `src/videos/<name>/`, register a new composition next to `BridgeShort` in `src/Root.tsx`, and rename it.
   - `SHOTS`: id, a/b frames, light day/golden, crowd mode, `tau` story time.
   - `XFADE`: crossfades at place/time changes.
   - `FLASH_AT`: a white flash after the hook.
   - `CAMS`: per-shot keys `{f, dur?, cut?, s: f => {pos, look, fov, roll}}`.
   - `KICKS`: impact flip-shakes.
   - `DOF`/`dofAt`: lens blur per beat.
   - `FOREGROUND`: near framing props.
   - Every visual reaction lands 0-3 frames before its word.
5. **World.**
   - `lights.ts`: LIGHTS plus the LOOK sky/river/cloud palette per light.
   - `shade.ts`: two-tone shading and `untone()`.
   - `build.ts`: town, houses and Kenney CC0 kit props, recoloured, with sight-line culling of anything blocking a camera.
   - `paint.ts`: HD Canvas2D painted textures with seams painted in as dark tints.
   - `world.ts`: sky shader, fog = horizon colour, river, per-frame posing, sun frozen per shot and camera-relative.
6. **Characters.**
   - `toon.ts`: the Canvas2D `Pen` drawing API, 600x1000 design canvas, soles at y = 975, bean heads, stick limbs, plum variable-width outline, face library.
   - `cast.ts`: camera-facing billboards, crowds, effect cards, blinks, walk cycles. All billboards go on the `NOINK` layer.
   - `cardshade.ts`: cards lit by the scene light, no emissive.
7. **Post** (`Bridge.tsx` + `ink.ts` + `lensblur.ts` + `grade.ts`).
   - Composer order: ink → lens pre → lens main → bloom → NEUTRAL tone map → grade (MSAA 4).
   - Every pixel parameter scales with `(output height / 1920)`.
8. **Sound** (`templates/audio/`: timeline.py, sfx_gen.py, sfx.py, music.py, instruments.py, dsp.py, mix.py).
   - Event table → synthesized SFX plus an original score ducked under the voice.
   - Output: `mix.wav` (48 kHz, exact length), stems, and `cues.md`.
   - Lock the picture's time constants before the sound is made. Any later timing change means re-running the sound.
9. **Look checks.** Run `node scripts/bridge-stills.mjs out/<name>/x_ 100,400 0.5`.
   - Set `BRIDGE_ENTRY=src/sandboxes/<n>/index.tsx` to render a sandbox copy.
   - Make side-by-sides against reference frames with `python scripts/sbs_sheet.py out.jpg --ours ... --ref ...`.
   - Send them to a Gemini Pro verification subagent: 1-3 images, a ≤200-word verdict, scoring 7 key categories.
10. **Final render.**
    - `npx remotion render src/index.ts <Comp> out/<name>/video.mp4 --codec h264 --crf 16 --scale 1.3333`
    - Mux with `-map 0:v:0 -map 1:a:0` (Remotion writes a silent audio track).
    - QA: `python scripts/short_qa.py final.mp4 out/<name>/qa shots.json` checks every frame for black, white, frozen and pop frames, plus loudness and sheets.
    - Fix anything it finds, then run a final Gemini Pro verification audit.
11. **Deliver.** Provide a clickable link to `final.mp4` ([final.mp4](file:///...)), generate an Antigravity walkthrough artifact with the QA metrics and score report, and present completion notes to the user.

## Final look values (bridge after 4 verifier rounds; all in `templates/bridge/`)
Start every new short from `templates/bridge/` (copy to `src/videos/<name>/`): the look lives in these values, the
story lives in `story.ts` / `build.ts` layout / `cast.ts` roles. Gemini Pro audit scores at the end: colour day 7, golden 5-6,
lighting 5-6, ink 6, textures 5-6, characters 7, depth 6-7, composition 6-7 (from 5/3/4/5/4/7/4/6 at the start).
- **Light presets** (`lights.ts`, sun camera-relative and frozen per shot):
  - day: az 75 / el 48, lit [1.58,1.5,1.33], shade [.30,.29,.36], lift [.05,.06,.11] (cool tint ONLY in shade), sky
    top #3e7fd2 → horizon #b8d0ec, fog = horizon, 25→300 m, uSat 1.08, ~15 % blue haze past 60 m.
  - golden: az 6 / el 7 (backlit low sun), key toward #FFB36B ×1.5, violet-blue shade (facade ≈ #444380), sky
    #ffc47c → #8a6f8a, peach fog only past 50 m, sun disc #ffcf9e + bloom, contact blobs + real card shadows.
- **Albedos** (`paint.ts`/`build.ts`): muted brick / cream / ochre / terracotta houses with plinth, cornice, sills,
  hoods, door step, chimney + pot, heights 7 / 8.4 / 9.8 m; warm grey/beige stone (saturation −35 % from "storybook");
  ochre wood deck C* ~51-58 with near-black seams; iron dark and desaturated. Never lemon, never lavender lit faces.
- **Ink** (`ink.ts`): #030303, 5.1 px near (6 m) → 3.3 px far (90 m) at 1080x1920, creases ×0.8 from 35°, depth
  jumps from 1 %, fog tint 0.3 only far; character cards on layer `NOINK` (they carry their own plum ink).
- **Lens** (`lensblur.ts` + `dofAt` in story.ts): cInf px at 1080: hook/river CU 15-16, close-ups 12-14, MS 10-12,
  park 7, golden sway 5, wides/aerials 0. Focus on the eyes of the front row.
- **Post** (`Bridge.tsx`): ink → lens pre → lens main → bloom (thr 1.0, int .5, 6 levels, radius .6) → NEUTRAL tone
  map → grade; MSAA 4. Film grain exists but is OFF (reference measures no grain; it quadruples the file size).
- **Characters** (`toon.ts`/`cast.ts`/`cardshade.ts`): bean heads h/w .94, plum ink #241726, eyes .26 W apart, no blush,
  14 expressions; adults 3.5 head-heights; walk bob 5 %, lean 1-7°, planted 0.8 m stride; blinks 0.5-2.3 s; tight
  contact shadow ~.5 under the feet + sun-direction tail by day; golden rim inner only (never an offset outer copy).
- **Camera** (`story.ts`): cuts on big jumps, smootherstep glides 18-40 f, every hold creeps (no static hold ≥4 f),
  flip kicks decaying over 7 f on impacts, 4-4.6° rolls, foreground props (`FOREGROUND`) in ~1/3 of shots.

## Look targets (measured from the reference; see `references/reports/`)
- **Ink:**
  - World lines: about 3 px at 1080 wide, near-black #0b0a0c, nearly constant with distance. Silhouettes, depth jumps and normal creases only. No line on wall/floor joins or the horizon. Character cards are never outlined by the world ink.
  - Character ink: dark plum #201628-#2f1d28, thicker on the bottom/shadow side.
- **Colour:**
  - Day median luma ~.57. Non-ink p5 ~.23 (no crushed blacks). Lit chroma C* p90 ~55. Day sky top ~#5e93d9, horizon 1.28x brighter.
  - Golden: peach horizon #ffd08a, violet-blue shadows (never brown), backlit sun.
- **Depth:**
  - DOF on about 1/3 of screen time (CU, MS, inserts), cInf 10-16 px at 1080, focus on the eyes. Establishing and wide shots stay sharp.
  - Fog = horizon colour, 25→420 m day, 20→360 m golden.
  - Bloom only on HDR emissives: threshold 1.0.
- **Camera:**
  - Hard cuts on big jumps. Everything else is a smootherstep glide of 18-40 f, peak ≤ 25 px/f at 720p.
  - Every hold pushes in 0.15-0.35 %/f, with 0.6 %/f on punch words.
  - Rolls of 4-5°.
  - No hand-held float. Impact shakes flip sign every frame and decay over 7 f.
- **Characters:**
  - About 3.5 head-heights tall, legs 1.4 HH.
  - Stick limbs about 0.055 of head width, ink-dot hands.
  - Bean head (h/w ~0.93, narrower chin, pointier crown).
  - No blush or eye highlights. Faces at brightness ~.93.
  - Walk bob 3-7 %, lean 1-7°, planted feet.
  - Blinks every 0.5-2.3 s, lasting 4 f.

## Antigravity Look-Match Loop & Swarm Orchestration

When conducting iterative look passes or "make it look like X" passes:
1. **Measure reference first.** Assign an analysis pass per topic (motion, depth, textures, characters, lighting, outlines, grade), writing numbers to `references/reports/<topic>.md`.
2. **Parallel Component Ownership (Swarm or Sandboxes):**
   When using Antigravity `swarm` or dedicated subagents, shard responsibilities by file ownership:
   - `cam`: `story.ts` (camera keys, cuts, kicks, DOF table, foreground props)
   - `world`: `world.ts`, `lights.ts`, `shade.ts`, `grade.ts` (sun, sky, fog, river, colour, grade)
   - `mat`: `paint.ts`, `build.ts` (painted textures, buildings, props)
   - `char`: `toon.ts`, `cast.ts`, `cardshade.ts` (character drawing, posing, card lighting, fx cards)
   - `post`: `ink.ts`, `Bridge.tsx`, `lensblur.ts` (outline pass, composer, lens blur, bloom)
   Each owner works cleanly without stepping on other components. In Antigravity `swarm`, use `workspace: "share"` for parallel authoring.
3. **Merge:** Run `python scripts/bridge_merge.py [cam,world,mat,char,post] --root <project-path>`.
   - Backs main up to `backup/bridge_<time>/`, copies owned files, then verify with `npx tsc --noEmit`.
4. **Verification with Gemini Pro:**
   - Generate side-by-side sheets: `python scripts/sbs_sheet.py out.jpg --ours a.jpg b.jpg --ref r1.jpg r2.jpg`
   - Launch or message a Gemini Pro verification subagent: pass the generated comparison image, and request scores across the 7 visual areas plus an actionable fix list with exact frame numbers.
   - Route fixes back to the component owners.
5. Contracts between owners live in exported constants (`NOINK` layer, `dofAt`/`FOREGROUND`, `LIGHTS`/`LOOK`).

## Gotchas & Production Traps
- **Kenney nature-kit materials are teal:** recolour them by material name in `build.ts`.
- **Cameras inside houses:** the sight-line culler in `build.ts`/`world.ts` removes geometry blocking camera rays.
- **Ink pass ordering:** Ink in the same merged effect pass as DOF gets overwritten. Ink MUST be its own pass before the blur.
- **Pixel scaling:** Pixel-sized post parameters must scale with resolution: stills are at 0.5, final at 1.333.
- **Disk & Bundling Cache:** Every Remotion bundle copies `public/` into the temp folder (`remotion-webpack-bundle-*`).
  - Set `REMOTION_TMP` to a drive with ample storage (e.g. `D:/remotion-tmp` or `C:/temp/remotion-tmp`).
  - When rendering is finished, clean up stale `remotion-webpack-bundle-*` and `puppeteer_dev_chrome_profile-*` directories.
- **Silent audio track:** Remotion writes a silent audio track by default: mux with ffmpeg using `-map 0:v:0 -map 1:a:0`.
- **Readability Traps:**
  - *Swing drawn with one rope reads as a hanging:* Always two ropes to a wide plank with the character seated between them (`swingKid` in `toon.ts`), and legs clearing the arc.
  - *Foreground props too close to lens (<2m):* Become huge cut-off blobs at frame edges. Re-check props when cameras move.
  - *Foreground bush cut by frame edge reads as "green ball":* Foreground prop must be instantly recognizable or omitted.
  - *Flags:* Avoid ambiguous modern looks; use historically accurate flags.
  - *Unlit signs:* Signs lit by side sun become muddy grey-blue; give sign faces unlit materials.
  - *Golden rim light:* Use inner rim light only on head/torso; never an offset outer copy (turns hats into picture frames).
  - *Railings at chest height:* Elevate camera to ~2.5 m so railings cross legs rather than chests.
  - *Static holds read as video freezes:* Every hold must have an active creeping push-in (0.15-0.35%/f).
