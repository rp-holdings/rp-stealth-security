import re

class ReconBarrier:
    MALICIOUS_PATTERNS = [
        re.compile(r"(\.\./|\.\.\)", re.IGNORECASE),
        re.compile(r"(union\s+select|select\s+.*\s+from|insert\s+into|drop\s+table)", re.IGNORECASE),
        re.compile(r"(<script|javascript:|onerror=)", re.IGNORECASE),
        re.compile(r"(etc/passwd|windows/win.ini|\.env|\.git)", re.IGNORECASE),
        re.compile(r"(wp-config\.php|phpinfo|eval\(|base64_decode)", re.IGNORECASE)
    ]
    @classmethod
    def is_suspicious(cls, path: str, query_string: str = "", body: str = "") -> bool:
        target = f"{path}?{query_string} {body}"
        return any(pattern.search(target) for pattern in cls.MALICIOUS_PATTERNS)
