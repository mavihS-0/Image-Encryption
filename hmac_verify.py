import hmac
import hashlib

def calculate_hmac(hmac_key, data):
    # Calculate HMAC using SHA-256
    h = hmac.new(hmac_key.encode(), data.encode(), hashlib.sha256)
    return h.hexdigest()

def verify_hmac(data, hmac_key, hmac_tag):
    # Calculate HMAC of data
    calculated_hmac = calculate_hmac(hmac_key, data)
    # Compare calculated HMAC with the provided HMAC tag
    return hmac.compare_digest(calculated_hmac, hmac_tag)