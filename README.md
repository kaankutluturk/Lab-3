# Lab III (formatted as a GitHub repo)

This repo organizes the "Lab III" handouts into a clean, repeatable structure and starts the work for each lab part (write-ups + commands + artifacts).

## Contents

- `01-info-gathering/` – Information gathering on `beuth-hochschule.de` using **theHarvester**
- `02-tls/` – TLS/HTTPS server security analysis (SSL Labs)
- `03-e2e-encryption/` – End-to-end encrypted email notes & comparison with TLS-only mail
- `04-reverse-engineering/` – Compile a C program and decompile the produced binary (RE workflow)
- `05-mobile-app-analysis/` – Static analysis of `app-release.apk` + OWASP checklist guidance
- `tools/` – Small helper utilities (binary Android XML → text)
- `assets/original/` – Unmodified original PDFs/XLSX/APK from the provided zip

## How to use

Each lab folder contains a `README.md` with:
1) what the handout asks for,
2) steps to reproduce the analysis,
3) findings / write-up (where already possible),
4) TODOs where the work requires an external environment (e.g., Kali, SSL Labs UI).

> Note: this repo is designed to be safe to share publicly (no credentials). If you add real harvested emails/names, consider storing them in a private repo.
