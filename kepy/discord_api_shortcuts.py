import requests
from kepy.settings.base import DISCORD_API, KEPY_TOKEN


def api_get(api_route: str, auth: str = None) -> "dict | None":
    if not auth:
        auth = f"Bot {KEPY_TOKEN}"
    r = requests.get(
        url=f"{DISCORD_API}{api_route}",
        headers={"Authorization": auth},
    )
    if r.status_code == 200:
        return r.json()
    else:
        return None


def api_put(api_route: str, reason: str = ""):
    return requests.put(
        url=f"{DISCORD_API}{api_route}",
        headers={"Authorization": f"Bot {KEPY_TOKEN}", "X-Audit-Log-Reason": reason},
    )


def api_delete(api_route: str, reason: str = ""):
    return requests.delete(
        url=f"{DISCORD_API}{api_route}",
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
