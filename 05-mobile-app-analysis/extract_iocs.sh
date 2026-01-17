#!/usr/bin/env bash
set -euo pipefail
APK_PATH="${1:-assets/original/Mobile App Analysis/app-release.apk}"
TMP_DIR="$(mktemp -d)"
trap 'rm -rf "$TMP_DIR"' EXIT

unzip -q "$APK_PATH" -d "$TMP_DIR"

echo "[+] Decoded manifest (high-level):"
python3 tools/axml2xml.py "$TMP_DIR/AndroidManifest.xml" | sed -n '1,120p'

echo
echo "[+] URLs found in classes.dex (ASCII scan):"
python3 - <<'PY'
import re
from pathlib import Path
b = Path("""'"""$TMP_DIR"""'"""/classes.dex").read_bytes()
urls=set()
for m in re.finditer(rb'(https?://[\x20-\x7e]{3,200})', b):
    u=m.group(1).decode('utf-8','ignore')
    u=re.split(r'[\x00\s"\']',u)[0]
    u=re.sub(r'^[0-9]+','',u)
    urls.add(u)
for u in sorted(urls):
    print(u)
PY
