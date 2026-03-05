import hashlib
import json

def compute_hash(file_path):
    with open(file_path, "rb") as f:
        data = f.read()
    return hashlib.sha256(data).hexdigest()

artifact_hash = compute_hash("sample_record.json")

print("Computed artifact hash:")
print(artifact_hash)

print("\nVerification step:")
print("Recompute canonical hash and compare to recorded artifact_hash.")
print("If hashes match and signature verifies, artifact integrity is confirmed.")
