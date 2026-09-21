#!/usr/bin/env python3
"""Create an example artifact using the canonical public CEYO Protocol v1 SDK.

Usage: pip install -r requirements.txt && python tools/make_example_artifact.py

Only public verification material is written. An ephemeral private signing key
remains in process memory and is not exported or committed to the site.
"""

from __future__ import annotations

import json
from pathlib import Path

from ceyo.keys import InMemoryKeyProvider
from ceyo.seal import seal_body


def main() -> None:
    out_dir = Path("example_artifact")
    out_dir.mkdir(parents=True, exist_ok=True)

    body = {
        "event": {
            "event_id": "site_demo_001",
            "type": "inference",
            "occurred_at": "2026-03-05T00:00:00Z",
            "request_id": "req-0001",
        },
        "policy": {"id": "site.example.capture", "version": "1.0"},
        "disclosure_tier": "public-demo",
    }
    signer = InMemoryKeyProvider()
    envelope = seal_body(body, key_provider=signer, validate=True)

    artifact_path = out_dir / "sealed_envelope.json"
    public_key_path = out_dir / "public_key.pem"
    artifact_path.write_text(json.dumps(envelope, indent=2) + "\n", encoding="utf-8")
    public_key_path.write_bytes(signer.get_public_key_pem())

    print(f"Generated {artifact_path} and {public_key_path}")
    print("The in-memory private key was not saved.")
    print(f"Verify: python tools/ceyo_verify.py {artifact_path} {public_key_path}")


if __name__ == "__main__":
    main()
