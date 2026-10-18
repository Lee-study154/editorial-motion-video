#!/usr/bin/env python3
"""Export the approved film's dependency closure, active assets, final mix and provenance."""
import argparse
import hashlib
import json
import re
import zipfile
from pathlib import Path

SKILL = Path(__file__).resolve().parents[1]
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument("project", type=Path, help="Original automation-video project root")
parser.add_argument("output", type=Path, help="New .zip archive; existing files are not overwritten")
args = parser.parse_args()
project = args.project.resolve()
output = args.output.resolve()
if output.exists():
    parser.error("Output exists; choose a new archive path")
source = project / "production/opener-preview"
files = {}
queue = [source / "src/FullFilmMaster.tsx"]
seen = set()
while queue:
    file = queue.pop()
    if file in seen:
        continue
    seen.add(file)
    text = file.read_text()
    files[str(file.relative_to(source))] = file.read_bytes()
    for dep in re.findall(r"(?:from\s+|import\s*)['\"](\.[^'\"]+)['\"]", text):
        base = file.parent / dep
        candidates = [base, *[Path(str(base) + ext) for ext in (".tsx", ".ts", ".js")]]
        match = next((p.resolve() for p in candidates if p.is_file()), None)
        if match is None:
            raise FileNotFoundError(f"Unresolved {dep} in {file}")
        queue.append(match)
asset_paths = list((source / "public/screens").glob("*"))
asset_paths += [source / "public/body/x-codex.jpg"]
asset_paths += list((source / "public/full").glob("*.png"))
for name in ("body", "head", "arm", "pupil-left", "pupil-right", "eyes-mask", "badge"):
    asset_paths.append(source / f"public/body-enhanced/character-{name}.png")
asset_paths += list((source / "public/body-enhanced").glob("page-*-cue.png"))
for file in asset_paths:
    if file.suffix.lower() in (".png", ".jpg", ".jpeg", ".svg", ".webp"):
        files[str(file.relative_to(source))] = file.read_bytes()
for name in ("package.json", "package-lock.json", "tsconfig.json"):
    files[name] = (source / name).read_bytes()
package = json.loads(files["package.json"])
package["scripts"] = {"typecheck": "tsc --noEmit", "still": "node render.mjs --still --frame 2406 --out out/still.png", "render": "node render.mjs --out out/film.mp4", "preview": "remotion studio src/example-index.tsx --no-open"}
files["package.json"] = json.dumps(package, indent=2).encode()
files["render.mjs"] = (SKILL / "assets/runtime/render.mjs").read_bytes()
files["render-config.json"] = json.dumps({"entry": "src/example-index.tsx", "composition": "AttentionMaster4K60", "audio": "audio/mix.m4a"}).encode()
files["src/example-index.tsx"] = b"""import {Composition,registerRoot} from 'remotion';
import {FullFilmMaster} from './FullFilmMaster';
import {FullFilmV3} from './FullFilmV3';
const Root=()=> <>
  <Composition id="AttentionMaster4K60" component={FullFilmMaster} width={1080} height={1920} fps={60} durationInFrames={2592} defaultProps={{shutterOffset:0}}/>
  <Composition id="AttentionFullFilmV3" component={FullFilmV3} width={1080} height={1920} fps={30} durationInFrames={1296} defaultProps={{shutterOffset:0}}/>
</>;
registerRoot(Root);
"""
files["audio/mix.m4a"] = (project / "production/full-film/ending-v3/audio/mix.m4a").read_bytes()
for name in ("audio_utils.py", "generate_score.py", "score.json"):
    files["audio/source/" + name] = (project / "production/full-film/audio" / name).read_bytes()
refs = [
    "production/body-preview/references/talkcraft/provenance.json",
    "production/opener-preview/audio/references/ATTRIBUTION.md",
    "production/full-film/references/intro-provenance.json",
    "production/full-film/references/outro-provenance.json",
    "production/full-film/ending-v3/references/onetake/case-source-manifest.json",
    "production/full-film/ending-v3/references/SELECTION.md",
    "production/full-film/master-4k60/reports/verification-master.json",
    "production/full-film/master-4k60/reports/REVIEW.md",
]
for file in source.glob("references/**/*.tsx"):
    if "ending-v2" not in file.parts:
        files[str(file.relative_to(source))] = file.read_bytes()
for relative in refs:
    files["provenance/" + relative.replace("/", "__")] = (project / relative).read_bytes()
# Archival exact-master route, preserving sibling layout inside legacy/.
master = (source / "scripts/render-master.mjs").read_text()
master = master.replace("import path from 'node:path';", "import path from 'node:path';\nimport {fileURLToPath} from 'node:url';\nimport {existsSync} from 'node:fs';")
master = master.replace("const root = process.cwd();", "const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '../..');")
master = master.replace("path.resolve(root, '../full-film/master-4k60')", "path.join(root, 'legacy/full-film/master-4k60')")
master = master.replace("const encoder = path.join(root,'node_modules/@remotion/compositor-darwin-arm64/ffmpeg');", "const bundledEncoder = path.join(root, `node_modules/@remotion/compositor-${process.platform}-${process.arch}/ffmpeg`);\nconst encoder = process.env.FFMPEG_EXECUTABLE || (existsSync(bundledEncoder) ? bundledEncoder : 'ffmpeg');")
master = re.sub(r"const python = [^;]+;", "const python = process.env.PYTHON_EXECUTABLE || 'python3';", master)
master = master.replace("const args = process.argv.slice(2);", "const chromePath = process.env.CHROME_PATH || '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome';\nif (!existsSync(chromePath)) throw new Error('Set CHROME_PATH to an installed Chrome; no download was attempted.');\nconst args = process.argv.slice(2);")
master = master.replace("browserExecutable:'/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',", "browserExecutable:chromePath,")
master = master.replace("entryPoint:path.join(root,'src/index.ts')", "entryPoint:path.join(root,'src/example-index.tsx')")
files["legacy/scripts/render-master.mjs"] = master.encode()
files["legacy/full-film/ending-v3/shutter_merge.py"] = (project / "production/full-film/ending-v3/shutter_merge.py").read_bytes()
files["legacy/full-film/ending-v3/audio/mix.m4a"] = files["audio/mix.m4a"]
# The archived probe compares the approved 60fps master against its 30fps source clock.
files["src/index.ts"] = b"import './example-index';\n"
files["PROVENANCE.md"] = (SKILL / "references/sources-and-boundaries.md").read_bytes()
files["REPRODUCE.md"] = (SKILL / "references/reproduce-example.md").read_bytes()
files["NOTICE.md"] = (SKILL / "NOTICE.md").read_bytes()
for notice in (SKILL / "licenses").glob("*.txt"):
    files["licenses/" + notice.name] = notice.read_bytes()
manifest = {name: hashlib.sha256(data).hexdigest() for name, data in sorted(files.items())}
files["source-hashes.json"] = json.dumps(manifest, indent=2).encode()
output.parent.mkdir(parents=True, exist_ok=True)
with zipfile.ZipFile(output, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=7) as archive:
    for name, data in sorted(files.items()):
        archive.writestr(name, data)
print(json.dumps({"status": "PASS", "archive": str(output), "files": len(files), "bytes": output.stat().st_size, "sourceModules": len(seen)}, indent=2))
