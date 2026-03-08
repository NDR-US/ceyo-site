Verification Walkthrough

This document demonstrates how a CEYO artifact can be independently verified using the reference verification tool provided in this repository.

The walkthrough illustrates how an external party can confirm the integrity of an artifact without access to the underlying AI system.

⸻

Overview

CEYO artifacts are designed to produce deterministic, cryptographically sealed records of AI system events.

Verification confirms three properties:
	1.	The artifact has not been modified
	2.	The artifact was generated according to the declared canonicalization rules
	3.	The artifact signature matches the verification key

Verification does not require access to model weights, inference infrastructure, or proprietary implementation details.

⸻

Example Files

The repository includes a minimal example artifact.

example_artifact/

sample_record.json
sample_signature.json
public_key.pem

These files represent:

sample_record.json
The canonical artifact record containing policy-scoped event data.

sample_signature.json
The digital signature generated for the artifact.

public_key.pem
The public verification key used to validate the signature.

⸻

Verification Procedure

The following steps illustrate how an independent verifier confirms the integrity of the artifact.

Step 1 — Load Artifact Record

The verifier loads the artifact record:

sample_record.json

This record contains the captured event data and metadata describing the artifact structure.

⸻

Step 2 — Canonicalize the Record

The artifact record is normalized using RFC 8785 JSON Canonicalization.

Canonicalization ensures that the JSON structure produces a deterministic byte representation.

This step guarantees that the same artifact always produces the same hash value when verified.

⸻

Step 3 — Generate Artifact Hash

Once canonicalized, the artifact is hashed using SHA-256.

The resulting digest represents the unique fingerprint of the artifact record.

If the artifact were modified in any way, the hash value would change.

⸻

Step 4 — Verify the Digital Signature

The artifact signature is validated using the provided public key.

Verification confirms that:
	•	the signature corresponds to the artifact hash
	•	the artifact was signed by the expected key

The reference implementation uses ECDSA with the P-256 curve.

⸻

Running the Verification Tool

Run the verification command:

python tools/ceyo_verify.py example_artifact/sample_record.json example_artifact/sample_signature.json example_artifact/public_key.pem

The verifier performs the following operations:
	•	RFC 8785 canonicalization
	•	SHA-256 hashing
	•	ECDSA-P256 signature verification

⸻

Expected Result

If the artifact is valid, the tool will report that the signature verification succeeded.

If the artifact has been modified, verification will fail.

Any change to the artifact record will alter the computed hash and invalidate the signature.

⸻

Independent Verification

The verification process does not require:
	•	access to the AI model
	•	access to training data
	•	access to proprietary system infrastructure

Any party with the artifact record, signature, and verification key can independently confirm artifact integrity.

⸻

Purpose of the Demonstration

This walkthrough demonstrates the core concept behind CEYO:

AI decision artifacts can be independently verified through deterministic canonicalization and cryptographic sealing.

This allows oversight, auditing, and post-incident review without requiring disclosure of proprietary AI system internals.

⸻

Related Documentation

See also:

docs/artifact-schema.json
docs/verification-protocol.md
docs/architecture.md
