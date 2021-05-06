import requests
from kepy.settings import API_BASE_URL, KEPY_TOKEN


def api_get(api_route: str) -> "dict | None":
    r = requests.put(
        url=f"{API_BASE_URL}{api_route}",
        headers={"Authorization": f"Bot {KEPY_TOKEN}"},
    )
    if r.status_code == 200:
        return r.json()
    else:
        return None


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


def get_user_from_api(user_id) -> "dict | None":
    """Gets an user from the api

    Args:
        user_id (int): The id of the user to retrieve

    Returns:
        dict: The user object
    """
    return api_get(api_route=f"/users/{user_id}")


def get_member_from_api(guild_id, member_id) -> "dict | None":
    """Gets an user from the api

    Args:
        user_id (int): The id of the user to retrieve

    Returns:
        dict: The user object
    """
    return api_get(api_route=f"/guilds/{guild_id}/members/{member_id}")
