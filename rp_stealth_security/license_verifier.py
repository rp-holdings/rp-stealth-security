import hmac
import hashlib

SECRET_SALT = b"RP_SEC_STEALTH_V9_SALT"

def verify_license(key: str) -> bool:
    if not key:
        return False
    parts = key.split("-")
    if len(parts) < 3 or parts[0] != "RPSEC":
        return False
    payload = f"{parts[0]}-{parts[1]}".encode()
    expected_sig = hmac.new(SECRET_SALT, payload, hashlib.sha256).hexdigest()[:12].upper()
    return hmac.compare_digest(parts[2], expected_sig)
