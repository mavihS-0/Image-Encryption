import random
import hashlib

def generate_private_key(p):
    # Generate a private key randomly in the range [1, p-2]
    return random.randint(1, p-2)

def compute_public_key(private_key,p,g):
    # Compute the public key using the given private key
    return pow(g, private_key, p)

def compute_shared_key(private_key, other_party_public_key,p):
    # Compute the shared key using the given private key and the other party's public key
    shared_value = pow(other_party_public_key, private_key, p)
    # Convert shared value to bytes
    shared_bytes = shared_value.to_bytes((shared_value.bit_length() + 7) // 8, byteorder='big')
    # Use a hashing algorithm (e.g., SHA-256) to derive a fixed-length shared key
    shared_key = hashlib.sha256(shared_bytes).digest()
    return shared_key

