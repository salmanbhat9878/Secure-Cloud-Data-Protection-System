import secrets
import hashlib
import hmac

def generate_capability_code():
    return secrets.token_urlsafe(32)

def hash_capability_code(code):
    return hashlib.sha256(code.encode()).hexdigest()

def verify_capability_code(code, stored_hash):
    if not code or not stored_hash:
        return False

    entered_hash = hash_capability_code(code)

    return hmac.compare_digest(entered_hash, stored_hash)