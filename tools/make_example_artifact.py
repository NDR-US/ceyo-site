#!/usr/bin/env python3
import base64
import hashlib
import json
from pathlib import Path

import rfc8785
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import ec


def b64u(data: bytes) -> str:
    return base64.urlsafe_b64encode(data).decode("ascii").rstrip("=")


def canonicalize(body) -> bytes:
    return rfc8785.dumps(body)


def main():
    out_dir = Path("example_artifact")
    out_dir.mkdir(parents=True, exist_ok=True)

    # 1) Generate keypair (P-256)
    priv = ec.generate_private_key(ec.SECP256R1())
    pub = priv.public_key()

    private_pem = priv.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption(),
    )
    public_pem = pub.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo,
    )

    # 2) Create a sample record (policy-scoped body)
    record = {
        "schema_version": "1.0",
        "ts": "2026-03-05T00:00:00Z",
        "policy": {"id": "POL-001", "version": "1.0"},
        "event": {
            "type": "inference",
            "model_ref": "opaque-ref",
            "request_id": "req-0001",
        },
        "env_fingerprint": "env:sha256:example",
        "input_ref_hash": "sha256:example",
        "output_ref_hash": "sha256:example",
    }

    # 3) Canonicalize + hash
    canonical = canonicalize(record)
    digest = hashlib.sha256(canonical).digest()

    # 4) Sign canonical bytes (DER ECDSA P-256)
    sig_der = priv.sign(canonical, ec.ECDSA(hashes.SHA256()))

    signature = {
        "hash": {"alg": "SHA-256", "value_b64u": b64u(digest)},
        "sig": {"alg": "ECDSA-P256-SHA256", "format": "DER", "value_b64u": b64u(sig_der)},
    }

    # 5) Write files
    (out_dir / "sample_record.json").write_text(json.dumps(record, indent=2), encoding="utf-8")
    (out_dir / "sample_signature.json").write_text(json.dumps(signature, indent=2), encoding="utf-8")
    (out_dir / "public_key.pem").write_bytes(public_pem)

    # Optional: private key for local testing ONLY (do not commit)
    (out_dir / "private_key.pem").write_bytes(private_pem)

    print("Wrote:")
    print(" - example_artifact/sample_record.json")
    print(" - example_artifact/sample_signature.json")
    print(" - example_artifact/public_key.pem")
    print(" - example_artifact/private_key.pem (DO NOT COMMIT)")


if __name__ == "__main__":
    main()
