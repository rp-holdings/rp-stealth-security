from typing import Dict, Any

class DecoyRouter:
    """
    Decoy Routing Engine: 攻撃者を隔離デコイ層へ透過的に転送
    """
    def __init__(self):
        self.quarantine_registry = set()

    def route_traffic(self, client_ip: str, is_threat: bool) -> Dict[str, Any]:
        if is_threat or client_ip in self.quarantine_registry:
            self.quarantine_registry.add(client_ip)
            return {
                "route": "decoy_sinkhole",
                "action": "isolate",
                "response_code": 404,
                "data_exposure": "zero"
            }
        return {
            "route": "primary_protected",
            "action": "pass",
            "response_code": 200,
            "data_exposure": "authorized"
        }
