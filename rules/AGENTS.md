# Animated Shorts Production Rules

When creating or modifying cartoon 3D animated shorts in this workspace or using this plugin, you MUST adhere to the following production rules:

## 1. Video Format & Technical Specs
- **Orientation & Dimensions**: Vertical 9:16.
  - Preview / Stills: 1080x1920 (scale 0.5 for fast still rendering).
  - Final Export: 2K vertical (1440x2560) rendered at `--scale 1.3333`, `--codec h264 --crf 16`.
- **Framerate**: Exactly 30 fps.
- **Duration**: ~55 to 70 seconds (median ~60 s, e.g. 1800-2100 frames).
- **Film Grain**: Kept OFF (grain quadruples file size and distorts on social video compression).

## 2. Text & Narrative Constraints
- **No On-Screen Captions**: Never burn in subtitles, captions, or text labels on screen unless explicitly requested by the user.
- **Language**: English only.
- **Voice Delivery**: One steady, fast narrator tone (3.5 to 4.1 words/s, median 3.7 words/s).
- **Facts & Humor**: Every joke is a researched historical or scientific fact. Never invent fake historical records.
- **Script Formula**:
  1. *Hook*: Paradox stated as fact in sentence 1 (~10-16 words).
  2. *Setting*: Year, place, concrete details.
  3. *Escalation*: 3-4 escalating beats.
  4. *Snap*: The breaking point / turning point.
  5. *Deadpan Double Line*: "Luckily ... / Unluckily ...".
  6. *Explanation*: Core physics/scientific mechanism explained through a simple everyday analogy.
  7. *Consequence*: The real-world rule or doctrine established.
  8. *Callback Twist*: Ending punchline.

## 3. Audio & Sound Mix
- **Mix Standards**:
  - Voice: Normalized to -14 LUFS integrated, unchanged in balance.
  - Music: Ducked under speech, standard level +3 dB relative to base bed.
  - SFX: Synthesized procedural effects, standard level -6 dB relative to base bed.
- **Timing Alignment**: Every visual reaction and sound cue lands 0 to 3 frames before its trigger word in `words.json`.
- **Locking**: Lock visual timings before final sound generation; timing changes require re-running `timeline.py` and `mix.py`.

## 4. Visual & Scene Construction
- **Character Layering**: Flat 2D bean-head characters (Canvas2D `toon.ts`) placed on camera-facing billboards in `cast.ts`. All character billboards MUST be placed on the `NOINK` layer so they carry only their custom plum ink outline.
- **Environment & Shading**: 3D Three.js environment with hand-painted Canvas2D textures (`paint.ts`), two-tone shading (`shade.ts`), and sight-line culling for cameras (`build.ts`).
- **Post-Processing Pipeline**:
  - Pass order in composer: `ink` -> `lens pre` -> `lens main` -> `bloom` -> `NEUTRAL tone map` -> `grade` (MSAA 4).
  - Ink MUST run as its own pass before depth of field (DOF) blur to prevent edge artifacts.
  - Pixel parameters must scale proportionally with `(output height / 1920)`.

## 5. Camera Motion Laws
- **Glide Transitions**: No hard cuts inside scenes unless deliberate; moves are smootherstep glides lasting 18 to 40 frames.
- **Active Holds**: Never allow a static hold of 4 frames or longer. Every hold MUST have a subtle creeping push-in (0.15% to 0.35% per frame; 0.6% on punch words).
- **Impact Kicks**: Decaying sign-flipping impact shakes over 7 frames on physical hits.
- **Lighting Dynamics**: Sun position is frozen camera-relative per shot.

## 6. Verification & Quality Assurance
- **Side-by-Side Review**: Generate stills and review them side-by-side with reference frames (`references/frames/`) using `sbs_sheet.py`.
- **Scoring**: Verification audits evaluate 7 core dimensions:
  1. Color (Day)
  2. Color (Golden)
  3. Lighting
  4. Ink Outlines
  5. Textures
  6. Characters
  7. Depth & Composition
- **Automated QA**: Run `short_qa.py` on the final render to check for black frames, unplanned white frames, frozen spans (>=12 frames), pop spikes, and audio loudness conformance.
