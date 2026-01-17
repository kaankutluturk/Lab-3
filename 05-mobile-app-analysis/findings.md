# Mobile app analysis findings (starter)

## 1) Information gathered (static)

- Package: `com.example2.tak.myprototype`
- Version: `1.0` (code 1)
- SDK: min 21, target 26
- Declared permission(s): INTERNET only
- UI: full-screen WebView
- Hardcoded URL (from DEX strings): `https://sites.google.com/view/prototype10/startseite`

## 2) Security observations / risks

- WebView wrapper apps inherit risk from remote content.
- Key things to verify in code (needs JADX/Ghidra):
  - Is JavaScript enabled?
  - Does the WebViewClient override SSL error handling?
  - Are file/content URL accesses enabled?
  - Is mixed content allowed?

## 3) Prevent APK installation

- User/device settings to block unknown sources
- Play Protect
- MDM allowlisting / policy enforcement
- Integrity checks (Play Integrity)

## 4) Difference vs iOS

- Distribution / sideloading constraints are stricter on iOS
- Mandatory code signing and tighter platform controls
- Reverse engineering still possible, but IPA/tooling + encryption/signing differ

## 5) Next steps

- Decompile with JADX: locate `MainActivity`, confirm what URL is loaded and what WebView settings are used.
- Dynamic analysis: run in emulator, capture traffic with a proxy, verify TLS pinning, see what endpoints are contacted.

