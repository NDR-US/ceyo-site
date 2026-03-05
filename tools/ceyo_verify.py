#!/usr/bin/env python3
"""
CEYO CLI Verifier

Usage:
  python tools/ceyo_verify.py record.json signature.json public_key.pem
  python tools/ceyo_verify.py envelope.json public_key.pem   (optional mode if you use a single envelope)

Outputs:
  PASS / FAIL / POLICY_MISMATCH
"""

import argparse
import json
import sys
from pathlib import Path

import rfc8785
from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import ec


def _read_text(p: Path) -> str:
    return p.read_text(encoding="utf-8")


def _read_json(p: Path):
    return json.loads(_read_text(p))


def _load_public_key(pem_path: Path) -> ec.EllipticCurvePublicKey:
    pub = serialization.load_pem_public_key(_read_text(pem_path).encode("utf-8"))
    if not isinstance(pub, ec.EllipticCurvePublicKey):
        raise TypeError("Expected an EC public key (P-256).")
    return pub


def _b64u_decode(s: str) -> bytes:
    s = s.strip()
    pad = "=" * ((4 - (len(s) % 4)) % 4)
    return __import__("base64").urlsafe_b64decode((s + pad).encode("ascii"))


def canonicalize_body(body) -> bytes:
    # RFC 8785 JCS canonical bytes
    return rfc8785.dumps(body)


def verify_record_and_signature(record_obj, sig_obj, public_key, expected_policy_id=None, expected_policy_version=None):
    """
    Assumes:
      - record_obj is the *body* (policy-scoped record)
      - sig_obj contains integrity fields:
          {
            "hash": {"alg":"SHA-256","value_b64u":"..."},
            "sig":  {"alg":"ECDSA-P256-SHA256","format":"DER","value_b64u":"..."}
          }
    """
    # Optional policy alignment check
    if expected_policy_id is not None or expected_policy_version is not None:
        pol = (record_obj.get("policy") or {})
        if expected_policy_id is not None and pol.get("id") != expected_policy_id:
            return ("POLICY_MISMATCH", f"Policy ID mismatch: expected {expected_policy_id}, got {pol.get('id')}")
        if expected_policy_version is not None and pol.get("version") != expected_policy_version:
            return ("POLICY_MISMATCH", f"Policy version mismatch: expected {expected_policy_version}, got {pol.get('version')}")

    canonical = canonicalize_body(record_obj)

    # Hash check (if provided)
    stored_hash = ((sig_obj.get("hash") or {}).get("value_b64u")) or None
    if stored_hash:
        import hashlib, base64
        digest = hashlib.sha256(canonical).digest()
        recomputed = base64.urlsafe_b64encode(digest).decode("ascii").rstrip("=")
        if recomputed != stored_hash:
            return ("FAIL", "Hash mismatch (record altered or wrong canonicalization).")

    # Signature check
    sig_info = sig_obj.get("sig") or {}
    sig_b64u = sig_info.get("value_b64u")
    if not sig_b64u:
        return ("FAIL", "Missing signature value_b64u.")
    sig_der = _b64u_decode(sig_b64u)

    try:
        public_key.verify(sig_der, canonical, ec.ECDSA(hashes.SHA256()))
    except InvalidSignature:
        return ("FAIL", "Signature validation failed.")
    except Exception as e:
        return ("FAIL", f"Verification error: {e}")

    return ("PASS", "Signature validated (and hash matched if present).")


def verify_envelope(envelope_obj, public_key, expected_product="CEYO", expected_policy_id=None, expected_policy_version=None):
    """
    Optional mode if you store a single envelope:
      {
        "product":"CEYO",
        "body":{...},
        "canonicalization":{ "scheme":"RFC8785", "scope":"body" },
        "integrity":{ "hash":{...}, "sig":{...} }
      }
    """
    if envelope_obj.get("product") != expected_product:
        return ("POLICY_MISMATCH", f"Product mismatch: expected {expected_product}, got {envelope_obj.get('product')}")
    body = envelope_obj.get("body")
    integrity = envelope_obj.get("integrity")
    if not isinstance(body, dict) or not isinstance(integrity, dict):
        return ("FAIL", "Malformed envelope (missing body/integrity).")
    return verify_record_and_signature(body, integrity, public_key, expected_policy_id, expected_policy_version)


def main():
    ap = argparse.ArgumentParser(prog="ceyo-verify", add_help=True)
    ap.add_argument("file1", help="record.json OR envelope.json")
    ap.add_argument("file2", help="signature.json OR public_key.pem (envelope mode)")
    ap.add_argument("file3", nargs="?", help="public_key.pem (record+signature mode)")
    ap.add_argument("--policy-id", default=None, help="Expected policy id (optional)")
    ap.add_argument("--policy-version", default=None, help="Expected policy version (optional)")
    ap.add_argument("--product", default="CEYO", help="Expected product marker (envelope mode)")
    args = ap.parse_args()

    f1 = Path(args.file1)
    f2 = Path(args.file2)

    if args.file3 is None:
        # envelope mode: file1=envelope.json, file2=public_key.pem
        envelope = _read_json(f1)
        pubkey = _load_public_key(f2)
        status, detail = verify_envelope(
            envelope, pubkey,
            expected_product=args.product,
            expected_policy_id=args.policy_id,
            expected_policy_version=args.policy_version
        )
    else:
        # record + signature mode: file1=record.json, file2=signature.json, file3=public_key.pem
        f3 = Path(args.file3)
        record = _read_json(f1)
        sig = _read_json(f2)
        pubkey = _load_public_key(f3)
        status, detail = verify_record_and_signature(
            record, sig, pubkey,
            expected_policy_id=args.policy_id,
            expected_policy_version=args.policy_version
        )

    print(status)
    print(detail)
    sys.exit(0 if status == "PASS" else 2)


if __name__ == "__main__":
    main()
