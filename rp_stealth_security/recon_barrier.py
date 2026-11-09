import time
from typing import Dict, Tuple

class ReconBarrier:
    """
    Reconnaissance Barrier: 外部スキャンおよび偵察プローブを低遅延で即時隔離
    """
    def __init__(self, rate_limit: int = 60, window_sec: int = 60):
        self.rate_limit = rate_limit
        self.window_sec = window_sec
        self.access_logs: Dict[str, list] = {}

    def is_probe_detected(self, client_ip: str, path: str, headers: dict) -> Tuple[bool, str]:
        now = time.time()
        
        # 悪意あるスキャンパス検知
        suspicious_paths = [".env", ".git", "wp-admin", "phpmyadmin", "shell", ".aws"]
        for sp in suspicious_paths:
            if sp in path.lower():
                return True, f"Suspicious reconnaissance path: {path}"

        # レートリミット検査
        history = self.access_logs.setdefault(client_ip, [])
        self.access_logs[client_ip] = [t for t in history if now - t < self.window_sec]
        self.access_logs[client_ip].append(now)

        if len(self.access_logs[client_ip]) > self.rate_limit:
            return True, "Rate limit threshold breached (Recon Probe)"

        return False, "Clear"
