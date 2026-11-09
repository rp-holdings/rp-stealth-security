import re
import hmac
import hashlib

class LicenseValidator:
    """
    RP Stealth Security V9 - ライセンス整合性検証エンジン
    """
    KEY_PATTERN = re.compile(r"^RP9-[0-9A-F]{8}-[0-9A-F]{8}-[0-9A-F]{8}-[0-9A-F]{8}$")

    @classmethod
    def validate_format(cls, key: str) -> bool:
        if not key or not isinstance(key, str):
            return False
        return bool(cls.KEY_PATTERN.match(key.strip()))

    @classmethod
    def verify_node(cls, license_key: str, node_id: str, signature: str, secret: str) -> bool:
        expected = hmac.new(
            secret.encode("utf-8"),
            f"{license_key}:{node_id}".encode("utf-8"),
            hashlib.sha256
        ).hexdigest()
        return hmac.compare_digest(expected, signature)
