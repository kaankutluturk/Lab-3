# Transport Layer Security (TLS)

**Task (from handout):** Check the server security of the website `beuth-hochshule.de` / `141.64.5.76` (likely intended: `beuth-hochschule.de`) and report the SSL Labs grade + why it is good/bad.

## How to run the check

Use SSL Labs "SSL Server Test":

- Enter the hostname (prefer **DNS name** over raw IP when possible; SNI and cert name matching matter).
- Re-run once if the first run is cached/outdated.

## What to report

SSL Labs breaks the grade into:
- **Certificate** (trusted CA, SANs, key size, chain)
- **Protocol Support** (TLS versions enabled)
- **Key Exchange** (PFS, DH params, ECDHE)
- **Cipher Strength** (modern suites)

Common grade killers
- Supporting **TLS 1.0 or TLS 1.1**: SSL Labs caps the grade to *B* when those are enabled.
- Weak ciphers (e.g., 3DES), no forward secrecy, or misconfigured chain.

## Suggested explanation template

Fill in your target's values:

- **Grade:** `__`
- **Why:**
  - TLS versions: `__`
  - Forward secrecy / ECDHE: `__`
  - Strong ciphers only: `__`
  - Valid, trusted certificate (no name mismatch): `__`
  - HSTS / OCSP stapling: `__`

## Evidence

Add screenshots of the SSL Labs results and paste any relevant config findings into `results.md`.
