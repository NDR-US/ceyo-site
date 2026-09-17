# CEYO

**Public presentation layer for independent evidentiary infrastructure for AI systems**

**Created and led by Brian Covarrubias**  
**Copyright © 2026 Brian Covarrubias. All rights reserved.**

Project site: https://ceyo.ai

## What CEYO is

CEYO is being developed as an independent evidentiary layer for consequential AI and autonomous-system operations.

Its purpose is to produce deterministic, cryptographically verifiable evidence artifacts that can be reviewed later without requiring access to model weights or proprietary system internals.

CEYO is deliberately separate from decision authority. It records and verifies evidence properties; it does not decide whether an underlying AI outcome was correct, fair, lawful, or institutionally sufficient.

## Current implementation and target architecture

CEYO is under active development.

The current public protocol profile demonstrates:

- policy-scoped structured artifact capture;
- RFC 8785 canonicalization;
- SHA-256 integrity digests;
- ECDSA P-256 / SHA-256 signatures;
- independent artifact verification;
- append-only storage primitives;
- Merkle-tree transparency logging, signed checkpoints, and inclusion proofs.

The broader target architecture extends this foundation toward protected policy/schema context, authenticated trust registries, hardware-backed key custody, trusted-time evidence, revocation, distributed transparency, constrained disclosure, custody, and institutional verification.

Future-state capabilities are design direction until they are formally specified, implemented, tested, and promoted into a versioned CEYO protocol profile.

## Protocol authority

This website is explanatory, not normative.

The canonical public CEYO protocol specification and reference implementation are maintained in:

- `NDR-US/ceyo-protocol`

Private architecture and research are maintained in:

- `NDR-US/ceyo-core`

The public decision demo is maintained in:

- `NDR-US/ceyo-decision-verification-demo`

If website language conflicts with a versioned protocol specification, the canonical protocol specification controls technical interpretation.

## Cryptographic roles

CEYO separates integrity, authenticity, confidentiality, trust, and time:

- hashing supports integrity comparison;
- digital signatures bind protected content to a cryptographic key holder;
- encryption, where used, protects confidentiality and is not itself the integrity validator;
- trust policy determines whether a signing key or authority is recognized;
- verifiable time/transparency evidence is required for stronger temporal claims.

## Claim boundaries

CEYO does not claim that cryptographic verification alone proves:

- the truth or completeness of pre-capture source data;
- model correctness or fairness;
- regulatory compliance;
- institutional authorization without a trust basis;
- real-world time of existence from an untrusted local timestamp;
- legal admissibility or evidentiary sufficiency.

CEYO produces verifiable evidence records, not judgments.

## This repository

`ceyo-site` contains the public-facing website, explanatory materials, sample artifacts, and selected demonstration tooling.

The site should not contain a competing protocol definition. Technical examples and terminology should remain aligned with `ceyo-protocol`.

## Versioning

Website release versions are presentation-layer versions and are distinct from protocol-profile versions. See `VERSION`, `VERSIONING.md`, and `CHANGELOG.md`.

## Authorship and ownership

CEYO was conceived and is directed by **Brian Covarrubias**. NDR-US is the GitHub publishing identity used for the project and should not be interpreted as a separate IP owner unless rights are formally assigned to a legal entity in the future.

See `LICENSE` for repository terms.
