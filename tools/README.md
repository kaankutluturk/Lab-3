# Tools

## axml2xml.py

Decodes Android binary XML (AXML) into readable XML.

Usage:

```bash
python tools/axml2xml.py <binary-xml-file>
```

Example:

```bash
python tools/axml2xml.py assets/original/Mobile\ App\ Analysis/app-release.apk
```

> Note: The script expects an extracted file (e.g., `AndroidManifest.xml`) not the APK directly.
