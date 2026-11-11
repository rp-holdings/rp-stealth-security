import re

class LicenseValidator:
    @staticmethod
    def validate(license_key: str) -> bool:
        if not license_key or not isinstance(license_key, str):
            return False
        pattern = r"^RP9-[A-F0-9]{8}-[A-F0-9]{8}-[A-F0-9]{8}-[A-F0-9]{8}$"
        return bool(re.match(pattern, license_key.strip()))
