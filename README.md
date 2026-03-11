# CEYO

Public website for CEYO — evidentiary infrastructure for AI-supported systems.

**Project site:**
https://ndr-us.github.io/ceyo-site/index.html

---

## What CEYO Is

CEYO is a conceptual evidentiary infrastructure for AI-supported decision systems.

It produces policy-scoped, deterministic, cryptographically sealed records of AI inference events. These records can be independently verified by any party who holds the sealed artifact and the corresponding public key — without access to model weights, proprietary internals, or the contents of the underlying decision.

CEYO operates outside the model. It does not modify, instrument, or interfere with AI inference. It records only what a governing capture policy explicitly permits.

---

## Why This Matters

AI systems increasingly influence consequential outcomes: credit, employment, healthcare, benefits, autonomous control. In regulated and high-stakes contexts, there is a distinct requirement that cannot be met by internal logging alone: the ability to demonstrate that a system behaved as declared, to an external party, without disclosing what it decided.

CEYO addresses this gap. A sealed artifact proves that a record was produced at a specific time, under a specific policy, and has not been altered since — without revealing what the underlying system processed or concluded.

---

## How It Works

Every CEYO artifact passes through a fixed lifecycle:

| Step | What happens |
|------|-------------|
| Policy-scoped capture | An inference event is recorded within the bounds of a declared capture policy; out-of-scope fields are excluded by design |
| Deterministic canonicalization | The captured body is serialized using RFC 8785 (JSON Canonicalization Scheme), producing identical bytes for identical inputs regardless of key ordering or whitespace |
| Cryptographic sealing | A SHA-256 hash and an ECDSA P-256 signature are computed over the canonical bytes |
| Independent verification | Any party with the sealed artifact and the corresponding public key can recompute the hash and validate the signature, with no access to the originating system |

---

## What CEYO Does Not Claim

CEYO is an evidentiary infrastructure. It is not:

- **A truth engine.** CEYO does not verify that an AI decision was correct.
- **A fairness engine.** CEYO does not assess whether a decision was equitable or unbiased.
- **A compliance certification.** CEYO does not certify conformance with any regulatory standard.
- **A model auditor.** CEYO does not access, analyze, or evaluate model internals.

CEYO proves that a sealed record is unaltered and was produced under a declared policy. It does not prove anything about the quality, legality, or appropriateness of the underlying AI output.

---

## This Repository

This repository is the **presentation layer** for CEYO. It contains the public-facing website explaining the concept, architecture, and verification approach.

**What is here:**
- Static website (HTML/CSS/JS)
- Interactive in-browser artifact verifier (`verify.html`)
- Reference implementation scripts for demonstration purposes (`tools/`, `example_artifact/`)

**What is not here:**
- Protocol specifications → maintained in `ceyo-protocol`
- Production SDK or deployment tooling

---

## Terminology

| Term | Meaning |
|------|---------|
| Policy-scoped capture | Recording only fields permitted by an explicit, declared capture policy |
| Deterministic canonicalization | Serialization that produces identical bytes for identical inputs (RFC 8785) |
| Sealed artifact | A JSON envelope containing a canonical body, its SHA-256 hash, and an ECDSA P-256 signature |
| Independent verification | Recomputing the hash and validating the signature using only the artifact and a public key |
| Constrained disclosure | Sharing verifiable evidence of behavior without exposing proprietary model internals |
| Tier | A declared disclosure level governing what the artifact conveys to a verifier |

---

## License

Copyright © 2026 Brian Covarrubias. All rights reserved.

This repository contains research materials, experimental code, and architectural concepts that are not licensed for reuse, modification, or commercial deployment without explicit written permission from the author.
