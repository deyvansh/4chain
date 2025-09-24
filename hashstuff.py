import hashlib
import os

hash_folder = "hashes"
os.makedirs(hash_folder, exist_ok=True)

def generate_hash(filepath):
    sha256_hash = hashlib.sha256()
    with open(filepath, "rb") as f:
        for byte_block in iter(lambda:f.read(4096), b""):
            sha256_hash.update(byte_block)
        return sha256_hash.hexdigest()
    
def save_hash(filename, file_hash):
    hash_filepath = os.path.join(hash_folder, f"{filename}.hash.txt")
    with open(hash_filepath, "w") as f:
        f.write(file_hash)
    return hash_filepath
