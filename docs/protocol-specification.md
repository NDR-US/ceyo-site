CEYO Protocol Specification

Version 0.1
CEYO Evidentiary Infrastructure Prototype

⸻

Abstract

CEYO defines a protocol for generating verifiable evidentiary artifacts from events produced by autonomous and AI-driven systems.

The protocol establishes a deterministic process for capturing policy-scoped event data, canonicalizing artifact records, generating cryptographic hashes, and applying digital signatures to produce tamper-evident records.

These artifacts enable independent verification of AI system outcomes without requiring access to model weights, proprietary inference infrastructure, or internal system implementation details.

⸻

Goals

The CEYO protocol is designed to support:

• independent verification of AI system outputs
• tamper-evident record generation
• deterministic artifact construction
• governance and oversight workflows

The protocol does not attempt to explain or interpret model behavior. It focuses solely on producing verifiable records of system events.

⸻

Design Principles

CEYO follows several core architectural principles.

Deterministic Artifact Generation
Artifacts must produce identical hashes when canonicalized under identical conditions.

Model Neutrality
The protocol does not modify, instrument, or depend on the underlying AI model.

Policy-Scoped Data Capture
Only explicitly declared fields are recorded in artifact records.

Independent Verification
Verification must be possible without access to proprietary system components.

Cryptographic Integrity
Artifacts must include cryptographic hashes and digital signatures.

⸻

Protocol Overview

The CEYO protocol defines a workflow consisting of three primary stages:

Record
Seal
Verify

Record
Policy-scoped event data is captured from an AI inference event.

Seal
The artifact record is canonicalized, hashed, and cryptographically signed.

Verify
An independent verifier recomputes the artifact hash and validates the signature.

⸻

Artifact Structure

Each CEYO artifact consists of a structured envelope containing several components.

Artifact Metadata
Identifiers and timestamps describing the event being recorded.

Policy Scope
Declarations describing which fields were captured.

Artifact Body
The captured event data.

Canonicalization Metadata
Information describing how the artifact body was normalized prior to hashing.

Cryptographic Integrity Fields
Hash values and digital signatures used to seal the artifact.

Verification References
Information required to obtain the appropriate verification key.

The formal artifact schema is defined in:

docs/artifact-schema.json

⸻

Canonicalization

Artifact records must be canonicalized prior to hashing.

CEYO uses deterministic JSON canonicalization based on RFC 8785.

Canonicalization ensures that:

• field ordering is consistent
• whitespace variations are removed
• equivalent JSON structures produce identical byte representations

This guarantees reproducible artifact hashes across independent verification environments.

⸻

Hash Generation

Once canonicalized, the artifact record is hashed using:

SHA-256

The resulting hash acts as a unique fingerprint of the artifact record.

Any modification to the artifact contents will result in a different hash value.

⸻

Digital Signatures

After hash generation, the artifact digest is signed using a digital signature algorithm.

Reference implementations may use:

ECDSA with the P-256 curve
or
RSA-PSS

The signature ensures that:

• the artifact hash originated from the signing entity
• the artifact has not been modified since signing

Verification keys may be distributed through trusted registries or infrastructure controlled by the deploying organization.

⸻

Verification Procedure

An independent verifier performs the following steps:

1 Load the artifact record
2 Canonicalize the artifact using RFC 8785
3 Compute the SHA-256 hash
4 Validate the digital signature using the verification key

If the computed hash matches the signed digest and the signature is valid, the artifact is considered authentic.

⸻

Independent Verification

The CEYO protocol is designed so that verification can occur without access to:

• model weights
• training data
• inference infrastructure
• proprietary system implementations

Verification requires only:

• the artifact record
• the artifact signature
• the verification key

⸻

Governance Considerations

CEYO separates artifact generation from governance functions.

The protocol itself does not interpret artifact data or make regulatory determinations.

Oversight responsibilities remain with external institutions such as:

• regulators
• auditors
• safety investigators
• compliance organizations

This separation preserves neutrality and avoids embedding governance authority within the infrastructure layer.

⸻

Security Considerations

CEYO artifacts provide tamper-evident records but do not guarantee correctness of the underlying AI decision.

Security risks that must be considered include:

• compromised signing keys
• incorrect policy configuration
• malicious or inaccurate event capture

Organizations implementing CEYO should ensure secure key management and carefully define artifact capture policies.

⸻

Future Work

Potential areas for further development include:

artifact registry infrastructure
distributed verification services
artifact timestamping systems
cross-system interoperability standards

Future versions of the protocol may refine artifact structure and verification procedures.

⸻

Status

This document describes an experimental protocol specification and reference architecture.

CEYO is currently a research prototype exploring evidentiary infrastructure for autonomous and AI-driven systems.
