# Reproduce the approved attention-economy film

The bundled example is a self-contained source/material snapshot: approved visual dependency closure, actual adapted components, final mixed audio, original procedural BGM source, provenance, media-review records and original-master rendering code. It is not the generic story template: its 43.2-second narrative is intentionally preserved.

```bash
python3 "$SKILL_DIR/scripts/init_project.py" /absolute/path/attention-example --example
cd /absolute/path/attention-example
```

Dependencies are pinned by package.json/package-lock.json. On a fresh computer use `npm ci` after explaining its dependency/disk impact. To reuse an already installed matching dependency tree with the generic renderer, set `EDITORIAL_NODE_MODULES=/absolute/path/existing/node_modules`. Set `CHROME_PATH` if needed; no browser or model is downloaded by these scripts.

## Fast preview / normal render

```bash
node render.mjs --still --frame 2406 --out out/ending.png
node render.mjs --out out/film.mp4
node render.mjs --scale 2 --out out/film-4k60.mp4
```

The example's composition uses 1080×1920 layout at 60fps. Scale 2 produces 2160×3840. The entry also registers the 30fps `AttentionFullFilmV3` source composition so the archived `--probe` can compare matching design times. This generic route preserves visual timing and muxes the approved 43.2-second mix, but does not perform the archival ending's multi-exposure shutter integration. Partial video ranges are intentionally silent when using this external final mix.

## Original master route (including ending shutter)

Run inside extracted example after dependencies are available in its own node_modules. Python requires NumPy and Pillow; ffmpeg is required. `PYTHON_EXECUTABLE` can select an existing Python runtime. `FFMPEG_EXECUTABLE` selects an encoder with libx264 and zscale; otherwise the script uses a matching existing Remotion compositor binary or system ffmpeg. This path performs the expensive original render; do not run it merely to inspect a frame.

```bash
node legacy/scripts/render-master.mjs --probe
node legacy/scripts/render-master.mjs
node legacy/scripts/render-master.mjs --ending
node legacy/scripts/render-master.mjs --assemble
```

Output: `legacy/full-film/master-4k60/attention-economy-4k60.mp4` and preview. The exported script replaces machine-specific Python/Chrome paths with environment options; layout and motion sources remain unchanged. Pixel-identical encodes across OS/browser versions are not promised; the original delivered master remains the archival approved export.

## Re-export from the original project

```bash
python3 "$SKILL_DIR/scripts/export_source.py" /absolute/path/original-project /absolute/path/new-example.zip
```

The exporter follows local imports starting at FullFilmMaster, includes the known dynamic asset families and final mix, and writes per-file SHA256 hashes. It excludes unused source roots, node_modules and caches. It is scoped to the approved film structure; inspect/update dynamic asset families if changing that structure. New films use the starter and new shot planning instead of global text replacement in this locked example.

## Original score source

`audio/source/generate_score.py` + `audio_utils.py` regenerate the original 43.2-second electronic bed (requires existing NumPy and ffmpeg). Run the generator from any directory; it writes beside itself. This is the approved film's fixed arrangement, not a general music-composition service. The final approved mix is already included; regeneration is optional. Separate third-party sound-library samples are not bundled.
