#!/usr/bin/env python3
"""Public v1 CEYO verification: delegate to the canonical Protocol verifier.

Usage: python tools/ceyo_verify.py <envelope.json> <public_key.pem>
This tool does not accept bare record/signature pairs or implement a second
canonicalization or signature profile. Install site requirements first.
"""

from __future__ import annotations

import argparse
import sys

from ceyo_verify.verifier import load_artifact, load_pubkey, verify_artifact


def main() -> int:
    parser = argparse.ArgumentParser(description="Verify a canonical public CEYO v1 artifact")
    parser.add_argument("envelope", help="Complete CEYO envelope JSON")
    parser.add_argument("public_key", help="PEM public verification key")
    parser.add_argument("--policy-id", help="Expected signed-body policy id")
    parser.add_argument("--policy-version", help="Expected signed-body policy version")
    args = parser.parse_args()

    try:
        artifact = load_artifact(args.envelope)
        public_key = load_pubkey(args.public_key)
        result = verify_artifact(artifact, public_key)
    except (OSError, ValueError, TypeError, KeyError) as exc:
        print(f"FAIL: Cannot load or verify CEYO artifact: {exc}", file=sys.stderr)
        return 2

    for message in result.passed:
        print(f"PASS: {message}")
    for message in result.failed:
        print(f"FAIL: {message}")

    if not result.ok:
        print("FAIL: Canonical CEYO verification failed")
        return 1

    policy = artifact.get("body", {}).get("policy") or {}
    if args.policy_id is not None and policy.get("id") != args.policy_id:
        print("POLICY_MISMATCH: Signed-body policy id differs from expected value")
        return 1
    if args.policy_version is not None and policy.get("version") != args.policy_version:
        print("POLICY_MISMATCH: Signed-body policy version differs from expected value")
        return 1

    print("PASS: Canonical CEYO v1 artifact verified (body-only signature scope)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
