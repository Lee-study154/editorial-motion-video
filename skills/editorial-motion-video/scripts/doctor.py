#!/usr/bin/env python3
"""Check project assets, timing, dependencies and supported content controls without installing anything."""
import argparse
import json
import os
import shutil
import subprocess
from pathlib import Path

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument("project", type=Path)
args = parser.parse_args()
root = args.project.resolve()
checks = []
def check(name, ok, detail):
    checks.append({"name": name, "ok": bool(ok), "detail": str(detail)})

for filename in ("package.json", "render-config.json", "render.mjs"):
    check(filename, (root / filename).is_file(), root / filename)
try:
    render = json.loads((root / "render-config.json").read_text())
    check("entry", (root / render["entry"]).is_file(), render["entry"])
    if render.get("audio"):
        check("approved-audio", (root / render["audio"]).is_file(), render["audio"])
    if (root / "project.json").exists():
        config = json.loads((root / "project.json").read_text())
        shots = config["shots"]
        valid = bool(shots) and all(s["seconds"] > 0 for s in shots)
        check("timing", valid, f"{sum(s['seconds'] for s in shots):.3f}s at {config['fps']}fps")
        check("shot-ids", len({s['id'] for s in shots}) == len(shots), "Shot IDs must be unique")
        total = sum(s["seconds"] for s in shots)
        ratio = sum(s["seconds"] for s in shots if s["kind"] == "illustration") / total
        check("illustration-share", ratio <= config["illustrationMax"], f"{ratio:.1%} / cap {config['illustrationMax']:.1%}")
        for item in shots + config.get("audio", []):
            asset = item.get("asset")
            if asset:
                check("asset", not asset.startswith(("http:", "https:")) and (root / "public" / asset).is_file(), asset)
        check("lead", config["lead"] in ("talkcraft", "onetake"), config["lead"])
except (OSError, ValueError, KeyError, ZeroDivisionError) as error:
    check("configuration", False, error)
node = shutil.which("node")
check("node", node, node or "Not found")
if node:
    modules = os.environ.get("EDITORIAL_NODE_MODULES", str(root / "node_modules"))
    script = "const{createRequire}=require('module');const r=createRequire(process.argv[1]);for(const p of ['@remotion/bundler','@remotion/renderer','react'])console.log(p,r.resolve(p));"
    result = subprocess.run([node, "-e", script, str(Path(modules).parent / "package.json")], capture_output=True, text=True)
    check("dependencies", result.returncode == 0, result.stdout.strip() or result.stderr.strip())
check("ffmpeg", shutil.which("ffmpeg"), shutil.which("ffmpeg") or "Needed for external-track mux")
candidates = ["/Applications/Google Chrome.app/Contents/MacOS/Google Chrome", "/usr/bin/google-chrome", "/usr/bin/chromium", "/usr/bin/chromium-browser"]
if os.environ.get("ProgramFiles"):
    candidates.append(str(Path(os.environ["ProgramFiles"]) / "Google/Chrome/Application/chrome.exe"))
chrome = os.environ.get("CHROME_PATH") or next((p for p in candidates if Path(p).is_file()), "")
check("browser", chrome and Path(chrome).is_file(), chrome or "Set CHROME_PATH to installed Chrome; no automatic download")
print(json.dumps({"status": "PASS" if all(c["ok"] for c in checks) else "FAIL", "checks": checks}, indent=2))
raise SystemExit(0 if all(c["ok"] for c in checks) else 1)
