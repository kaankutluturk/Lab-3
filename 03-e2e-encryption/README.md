# End-to-End Encryption (E2EE) in Email

**Goal:** send an end-to-end encrypted email (e.g., Proton Mail or Tutanota) and explain why E2EE is stronger than "TLS-only" email.

## Deliverables

1. Screenshot (or short description) of sending an encrypted message.
2. A short comparison: E2EE vs TLS.

## Why E2EE is better than TLS-only

- **TLS-only** protects the hop between mail clients/servers (in transit). The message is typically decrypted on each server hop and stored plaintext-accessible to the provider.
- **E2EE** encrypts on the sender device and can only be decrypted by the intended recipient, so the provider and intermediate servers cannot read the content (assuming keys are handled correctly).

## Common points to mention

- Threat model: provider compromise, insider access, lawful access requests.
- Key management: passwords/keys, recovery options.
- Metadata: E2EE protects content, but headers/metadata (to/from/time) are often still visible.

## Suggested write-up

Use `results.md` to describe:
- Which provider/client you used
- How encryption was enabled
- What the recipient needed to decrypt
- What is and isn’t protected
