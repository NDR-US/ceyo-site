"""
CEYO: Simplified educational demo.

Uses ECDSA P-256 + SHA-256 for consistency with the reference implementation.
For production use with RFC 8785 JSON canonicalization, see ceyo_reference_implementation.py.
"""

import base64
import hashlib
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import ec


# --- CEYO LAYER 1: CANONICALIZATION (The 'Seal') ---
def ceyo_canonicalize(text):
    """
    Encodes the input as UTF-8 bytes — the canonical form for this demo.

    Note: for structured JSON artifacts, the reference implementation applies
    RFC 8785 (JCS) canonicalization before hashing, ensuring deterministic
    serialization regardless of key ordering or whitespace.
    """
    return text.encode("utf-8")


# --- CEYO LAYER 2: CRYPTOGRAPHIC SIGNING ---
def ceyo_sign(data, private_key):
    """
    Signs the canonical bytes using ECDSA P-256 / SHA-256.
    Returns a base64url-encoded DER signature.
    """
    sig_der = private_key.sign(data, ec.ECDSA(hashes.SHA256()))
    return base64.urlsafe_b64encode(sig_der).decode("ascii").rstrip("=")


# --- CEYO LAYER 3: INDEPENDENT VERIFICATION ---
def ceyo_verify(data, signature_b64u, public_key):
    """
    Verifies an ECDSA P-256 signature over the canonical bytes.
    Returns True if authentic, False if tampered or invalid.
    """
    padded = signature_b64u + "=" * ((4 - len(signature_b64u) % 4) % 4)
    sig_der = base64.urlsafe_b64decode(padded)
    try:
        public_key.verify(sig_der, data, ec.ECDSA(hashes.SHA256()))
        return True
    except Exception:
        return False


# --- DEMO ---

if __name__ == "__main__":
    print("--- CEYO INFRASTRUCTURE DEMO ---\n")

    # 1. Generate a P-256 keypair (production: operator HSM/KMS; CEYO stays non-custodial)
    private_key = ec.generate_private_key(ec.SECP256R1())
    public_key = private_key.public_key()

    # 2. The AI Generation Event
    ai_output = "CEYO provides a deterministic evidentiary record for this AI response."
    print(f"[AI OUTPUT]: {ai_output}")

    # 3. Sealing the Evidence
    canonical = ceyo_canonicalize(ai_output)
    hash_hex = hashlib.sha256(canonical).hexdigest()
    digital_seal = ceyo_sign(canonical, private_key)
    print(f"[SHA-256]:   {hash_hex[:20]}...")
    print(f"[CEYO SEAL]: {digital_seal[:40]}...")

    # 4. Verification Check
    is_authentic = ceyo_verify(canonical, digital_seal, public_key)
    print(f"\n[VERIFICATION STATUS]: {'VALID & UNTAMPERED' if is_authentic else 'TAMPERED/INVALID'}")

    # 5. Tamper Test (simulating an alteration)
    tampered = ceyo_canonicalize("The AI company is NOT liable.")
    is_still_authentic = ceyo_verify(tampered, digital_seal, public_key)
    print(f"[TAMPER TEST STATUS]:  {'VALID' if is_still_authentic else 'REJECTED (Tamper Detected)'}")
