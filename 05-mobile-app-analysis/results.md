# Mobile App Analysis – Results

## App fingerprint

See `analysis/apk_fingerprint.txt`.

## Static findings

- Package name: `com.example2.tak.myprototype`
- Main activity: `com.example2.tak.myprototype.MainActivity`
- Permissions: `INTERNET`
- Layout: full-screen `WebView`
- URL loaded: `https://sites.google.com/view/prototype10/startseite`

## OWASP MSTG checklist notes

Use the Excel checklist in `assets/original/Mobile App Analysis/Mobile_App_Security_Checklist.xlsx` and record:

- MSTG-STORAGE: __
- MSTG-NETWORK: __
- MSTG-CRYPTO: __
- MSTG-PLATFORM: __
- MSTG-CODE: __
- MSTG-RESILIENCE: __

## Recommended next steps (if you have tools)

- Decompile with `jadx-gui` or `jadx -d out app-release.apk`
- Inspect WebView settings: JavaScript enabled? file access? mixed content? navigation restrictions?
- Dynamic test with a proxy (Burp) + emulator to confirm traffic and certificate pinning
