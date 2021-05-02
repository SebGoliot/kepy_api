import requests
from kepy.settings import API_BASE_URL, KEPY_TOKEN


def api_put(api_route: str, reason: str = ""):
    return requests.put(
        url=f"{API_BASE_URL}{api_route}",
        headers={"Authorization": f"Bot {KEPY_TOKEN}", "X-Audit-Log-Reason": reason},
    )


def api_delete(api_route: str, reason: str = ""):
    return requests.delete(
        url=f"{API_BASE_URL}{api_route}",
        headers={"Authorization": f"Bot {KEPY_TOKEN}", "X-Audit-Log-Reason": reason},
    )
