"""
CEYO: Evidentiary Infrastructure for Autonomous Systems
Reference Implementation (v1.0)

Copyright © 2026 Brian Covarrubias. All Rights Reserved.
Not licensed for reuse, modification, or commercial deployment without explicit written permission.
Design: Policy-scoped, canonical artifacts via RFC 8785 and ECDSA P-256.
"""
"""
CEYO-style sealing + independent verification (reference implementation)

Design goals (matching your stated posture):
- Policy-scoped, canonical artifacts (RFC 8785 / JCS canonicalization)
- Deterministic hashing (SHA-256 of canonical bytes)
- Cryptographic sealing (ECDSA P-256 over canonical bytes)
- Non-adjudication: verification confirms integrity + declared policy alignment only
- Explicit boundaries: signature covers *body only*; envelope is not signed

Install:
  pip install rfc8785 cryptography
"""

import base64
import hashlib
from dataclasses import dataclass
from enum import Enum
from typing import Any, Dict, Optional

import rfc8785
from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import ec


# ----------------------------
# Utilities
# ----------------------------

def b64u(data: bytes) -> str:
    """Base64url without padding."""
    return base64.urlsafe_b64encode(data).decode("ascii").rstrip("=")

def b64u_decode(s: str) -> bytes:
    """Decode base64url without padding."""
    padded = s + "=" * ((4 - len(s) % 4) % 4)
    return base64.urlsafe_b64decode(padded.encode("ascii"))

def canonicalize_rfc8785(json_value: Any) -> bytes:
    """
    RFC 8785 (JCS) canonical serialization of a JSON value.
    Returns canonical UTF-8 bytes.
    """
    return rfc8785.dumps(json_value)

def sha256_digest(data: bytes) -> bytes:
    return hashlib.sha256(data).digest()


# ----------------------------
# Signing / Verification
# ----------------------------

def sign_ecdsa_p256_der(message: bytes, private_key_pem: str) -> bytes:
    """
    ECDSA P-256 signature over message bytes, hashed with SHA-256.
    Output is ASN.1 DER-encoded signature bytes.
    """
    private_key = serialization.load_pem_private_key(private_key_pem.encode("utf-8"), password=None)
    if not isinstance(private_key, ec.EllipticCurvePrivateKey):
        raise TypeError("Expected an EC private key (P-256).")
    return private_key.sign(message, ec.ECDSA(hashes.SHA256()))

def verify_ecdsa_p256_der(message: bytes, sig_der: bytes, public_key_pem: str) -> bool:
    public_key = serialization.load_pem_public_key(public_key_pem.encode("utf-8"))
    if not isinstance(public_key, ec.EllipticCurvePublicKey):
        raise TypeError("Expected an EC public key (P-256).")
    try:
        public_key.verify(sig_der, message, ec.ECDSA(hashes.SHA256()))
        return True
    except InvalidSignature:
        return False


# ----------------------------
# Verification outcomes
# ----------------------------

class VerificationStatus(str, Enum):
    INTEGRITY_CONFIRMED = "Integrity Confirmed"
    INTEGRITY_FAILED = "Integrity Failed"
    POLICY_SCOPE_MISMATCH = "Policy Scope Mismatch"

@dataclass
class VerificationResult:
    status: VerificationStatus
    detail: str


# ----------------------------
# CEYO envelope format
# ----------------------------

def seal_artifact_body(
    body: Dict[str, Any],
    private_key_pem: str,
    *,
    product: str = "CEYO",
    suite: str = "ECDSA-P256-SHA256",
    canonicalization_scheme: str = "RFC8785",
    canonicalization_version: str = "1.0",
) -> Dict[str, Any]:
    """
    Returns a sealed envelope:
      {
        "product": "CEYO",
        "body": { ... policy-scoped canonical artifact ... },
        "canonicalization": { ... },
        "integrity": { hash, sig, suite metadata }
      }

    Signature covers canonicalized bytes of envelope["body"] only.
    """
    canonical_body = canonicalize_rfc8785(body)
    digest = sha256_digest(canonical_body)
    sig_der = sign_ecdsa_p256_der(canonical_body, private_key_pem)

    envelope = {
        "product": product,
        "body": body,
        "canonicalization": {
            "scheme": canonicalization_scheme,
            "version": canonicalization_version,
            "scope": "body",
        },
        "integrity": {
            "hash": {
                "alg": "SHA-256",
                "value_b64u": b64u(digest),
                "covers": "canonical(body)",
            },
            "sig": {
                "alg": suite,
                "format": "DER",
                "value_b64u": b64u(sig_der),
                "covers": "canonical(body)",
            },
        },
    }
    return envelope


def verify_sealed_envelope(
    envelope: Dict[str, Any],
    public_key_pem: str,
    *,
    expected_policy_id: Optional[str] = None,
    expected_policy_version: Optional[str] = None,
    expected_product: str = "CEYO",
) -> VerificationResult:
    """
    Independent verification workflow:
      1) Product marker check (optional)
      2) Policy alignment check (optional)
      3) Canonicalize envelope["body"] under RFC 8785
      4) Recompute SHA-256 and compare to stored hash
      5) Validate ECDSA signature over canonical(body)
      6) Return:
         - Integrity Confirmed
         - Integrity Failed
         - Policy Scope Mismatch
    """
    if not isinstance(envelope, dict) or "body" not in envelope or "integrity" not in envelope:
        return VerificationResult(VerificationStatus.INTEGRITY_FAILED, "Malformed envelope (missing body/integrity).")

    if envelope.get("product") != expected_product:
        return VerificationResult(
            VerificationStatus.POLICY_SCOPE_MISMATCH,
            f"Product marker mismatch (expected {expected_product}, got {envelope.get('product')}).",
        )

    body = envelope["body"]
    integrity = envelope.get("integrity", {})
    canon_meta = envelope.get("canonicalization", {})

    if canon_meta.get("scheme") != "RFC8785" or canon_meta.get("scope") != "body":
        return VerificationResult(
            VerificationStatus.INTEGRITY_FAILED,
            "Unsupported or unclear canonicalization metadata (expected RFC8785 over body).",
        )

    # Policy alignment check
    policy = body.get("policy", {})
    body_policy_id = policy.get("id")
    body_policy_ver = policy.get("version")

    if expected_policy_id is not None and body_policy_id != expected_policy_id:
        return VerificationResult(
            VerificationStatus.POLICY_SCOPE_MISMATCH,
            f"Policy ID mismatch (expected {expected_policy_id}, got {body_policy_id}).",
        )
    if expected_policy_version is not None and body_policy_ver != expected_policy_version:
        return VerificationResult(
            VerificationStatus.POLICY_SCOPE_MISMATCH,
            f"Policy version mismatch (expected {expected_policy_version}, got {body_policy_ver}).",
        )

    canonical_body = canonicalize_rfc8785(body)

    # Hash check
    stored_hash_b64u = integrity.get("hash", {}).get("value_b64u")
    if not isinstance(stored_hash_b64u, str) or not stored_hash_b64u:
        return VerificationResult(VerificationStatus.INTEGRITY_FAILED, "Missing stored hash.")

    recomputed_digest = sha256_digest(canonical_body)
    if b64u(recomputed_digest) != stored_hash_b64u:
        return VerificationResult(VerificationStatus.INTEGRITY_FAILED, "Hash mismatch (artifact altered or malformed).")

    # Signature check
    sig_info = integrity.get("sig", {})
    if sig_info.get("alg") != "ECDSA-P256-SHA256" or sig_info.get("format") != "DER":
        return VerificationResult(VerificationStatus.INTEGRITY_FAILED, "Unsupported signature suite/format.")

    sig_b64u = sig_info.get("value_b64u")
    if not isinstance(sig_b64u, str) or not sig_b64u:
        return VerificationResult(VerificationStatus.INTEGRITY_FAILED, "Missing signature.")

    sig_der = b64u_decode(sig_b64u)
    ok = verify_ecdsa_p256_der(canonical_body, sig_der, public_key_pem)
    if not ok:
        return VerificationResult(VerificationStatus.INTEGRITY_FAILED, "Signature validation failed.")

    return VerificationResult(VerificationStatus.INTEGRITY_CONFIRMED, "Hash and signature validated under declared policy.")


# ----------------------------
# Example usage
# ----------------------------

if __name__ == "__main__":
    # Generate a P-256 keypair (production: operator HSM/KMS/TEE; CEYO stays non-custodial)
    priv = ec.generate_private_key(ec.SECP256R1())
    private_pem = priv.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption(),
    ).decode("utf-8")
    public_pem = priv.public_key().public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo,
    ).decode("utf-8")

    # Policy-scoped artifact body (this is what gets canonicalized + signed)
    body = {
        "ts": "2026-03-01T00:00:00Z",
        "policy": {"id": "POL-001", "version": "1.0"},
        "tier": "controlled",
        "env_fingerprint": "env:sha256:7b2c...(example)",
        "input_ref_hash": "sha256:1a9f...(example)",
        "event": {"type": "inference", "model_ref": "opaque-ref"},
    }

    sealed = seal_artifact_body(body, private_pem)

    result = verify_sealed_envelope(
        sealed,
        public_pem,
        expected_policy_id="POL-001",
        expected_policy_version="1.0",
        expected_product="CEYO",
    )

    print("Verification:", result.status.value)
    print("Detail:", result.detail)
    print("Sealed envelope keys:", list(sealed.keys()))
