# Mobile App Analysis (Android APK)

APK: `assets/original/Mobile App Analysis/app-release.apk`

## What we can already see (offline static)

### Manifest highlights

Decoded with `tools/axml2xml.py`:

- **Package:** `com.example2.tak.myprototype`
- **minSdk/targetSdk:** 21 / 26 (Android 5.0 → 8.0)
- **Permissions:** `android.permission.INTERNET` only
- **allowBackup:** `true` (ADB backup / some device backups may include app data)
- **Main activity:** `com.example2.tak.myprototype.MainActivity`

See: `analysis/AndroidManifest.xml.decoded.xml`

### UI/layout

`res/layout/activity_main.xml` is essentially a full-screen **WebView**.

See: `analysis/activity_main.xml.decoded.xml`

### Network endpoints

The DEX strings include:
- `https://sites.google.com/view/prototype10/startseite`

This strongly suggests the app is a simple WebView wrapper around that site.

## Questions from the lab

### 1) Which information can you gather?

Typical items from an APK (even without dynamic analysis):
- App identity (package, version, SDK levels)
- Permissions and exported components
- Hardcoded URLs/endpoints, API keys, feature flags
- Use of WebView, third-party SDKs, analytics libraries
- Potential data storage choices (shared prefs/SQLite) once decompiled/dynamic-tested

### 2) How to prevent APK installations?

Android controls (choose relevant for your scenario):
- Disable "Install unknown apps" / "Unknown sources"
- Enforce **Play Protect** and require installs via managed Play Store
- MDM/EMM policies (work profiles) to block sideloading
- App whitelisting / allow-listing + verified boot / device integrity checks

### 3) Difference compared to iOS apps?

High-level differences:
- iOS generally restricts sideloading more (App Store + signing, enterprise profiles, etc.), while Android historically allowed sideloading more easily.
- iOS apps use IPA + strong code signing + entitlements; Android uses APK + manifest permissions and (optionally) signature-level permissions.
- Reverse engineering differs: Android bytecode (DEX) is commonly decompiled; iOS binaries are native (Mach-O) and RE is more like classic native reversing.

## OWASP checklist

Use the provided checklist in `assets/original/Mobile App Analysis/Mobile_App_Security_Checklist.xlsx` and record findings in `results.md`.
