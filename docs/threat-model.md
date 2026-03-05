# CEYO Threat Model

## Security Goals

CEYO artifacts are designed to provide tamper-evident records
of AI system events that can be independently verified.

Primary security goals:

• Artifact integrity
• Artifact authenticity
• Policy scope transparency
• Independent verification capability

## Threat Scenarios

### Artifact Tampering
An attacker modifies the artifact body after generation.

Mitigation:
Cryptographic hashing and digital signatures.

### Replay Attacks
A valid artifact is reused in a different context.

Mitigation:
Timestamp and environment fingerprint fields.

### Key Substitution
An attacker replaces the public verification key.

Mitigation:
Trusted key registry or known verification authority.
