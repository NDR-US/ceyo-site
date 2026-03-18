"""
Verify a CEYO sealed envelope from the command line.

Usage:
    python verify_artifact.py sealed_envelope.json public_key.pem

This mirrors the three-step workflow in tools/ceyo_reference_implementation.py:
  1. RFC 8785 canonicalize envelope["body"]
  2. Recompute SHA-256 and compare to integrity.hash.value_b64u
  3. Validate ECDSA P-256 signature over canonical bytes

Generate a real signed artifact first:
    cd ..
    pip install rfc8785 cryptography
    python tools/make_example_artifact.py
"""

import base64
import hashlib
import json
import sys
from pathlib import Path

import rfc8785
from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import ec


def b64u_decode(s: str) -> bytes:
    padded = s + "=" * ((4 - len(s) % 4) % 4)
    return base64.urlsafe_b64decode(padded.encode("ascii"))


def main(envelope_path: str, public_key_path: str) -> None:
    envelope = json.loads(Path(envelope_path).read_text(encoding="utf-8"))
    public_key_pem = Path(public_key_path).read_bytes()

    body = envelope["body"]
    integrity = envelope["integrity"]
    canon_meta = envelope.get("canonicalization", {})

    if canon_meta.get("scheme") != "RFC8785" or canon_meta.get("scope") != "body":
        print("FAIL: unsupported canonicalization metadata.")
        sys.exit(1)

    # Step 1: canonicalize
    canonical = rfc8785.dumps(body)

    # Step 2: hash check
    computed = base64.urlsafe_b64encode(hashlib.sha256(canonical).digest()).decode("ascii").rstrip("=")
    stored = integrity["hash"]["value_b64u"]
    if computed != stored:
        print(f"FAIL: hash mismatch.\n  computed: {computed}\n  stored:   {stored}")
        sys.exit(1)
    print(f"PASS: hash matched  ({computed[:20]}...)")

    # Step 3: signature check
    sig_info = integrity["sig"]
    if sig_info.get("alg") != "ECDSA-P256-SHA256" or sig_info.get("format") != "DER":
        print("FAIL: unsupported signature suite.")
        sys.exit(1)

    sig_der = b64u_decode(sig_info["value_b64u"])
    public_key = serialization.load_pem_public_key(public_key_pem)
    if not isinstance(public_key, ec.EllipticCurvePublicKey):
        print("FAIL: expected an EC public key.")
        sys.exit(1)

    try:
        public_key.verify(sig_der, canonical, ec.ECDSA(hashes.SHA256()))
        print("PASS: signature valid")
        print("RESULT: Integrity Confirmed")
    except InvalidSignature:
        print("FAIL: signature invalid")
        sys.exit(1)


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python verify_artifact.py <envelope.json> <public_key.pem>")
        sys.exit(1)
    main(sys.argv[1], sys.argv[2])
