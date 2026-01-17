# Status

What’s already done in this repo:

- ✅ Materials reorganized and cleaned (MacOSX artifacts removed).
- ✅ Added `tools/axml2xml.py` to decode Android binary XML.
- ✅ Per-task writeup stubs created with reproduction steps.
- ✅ Started static analysis of `app-release.apk` (manifest + layout + endpoint string).

What still requires running externally (not possible to fully reproduce in this sandbox):

- theHarvester live OSINT pulls (depends on search engines/rate limits)
- Qualys SSL Labs live TLS grading for the target host
- Decompilation with radare2/jadx/apktool (tools not installed in this environment)
