import requests
from kepy.settings.base import DISCORD_API, KEPY_TOKEN


def api_get(api_route: str, auth: str = None) -> dict:
    """Gets an object from the api

    Args:
        api_route (str): The api route to get the object from
        auth (str, optional): The auth token. Defaults to None.

    Returns:
        dict: The object
    """
    if not auth:
        auth = f"Bot {KEPY_TOKEN}"
    r = requests.get(
        url=f"{DISCORD_API}{api_route}",
        headers={"Authorization": auth},
    )
    if r.status_code != 200:
        raise Exception(
            f"GET request returned {r.status_code} code: expected 200\n{r}"
        )
    return r.json()


def api_put(api_route: str, reason: str = "") -> None:
    """Puts an object to the api

    Args:
        api_route (str): The api route to put the object to
        reason (str, optional): The reason of the action. Defaults to "".
    """
    r = requests.put(
        url=f"{DISCORD_API}{api_route}",
        headers={"Authorization": f"Bot {KEPY_TOKEN}", "X-Audit-Log-Reason": reason},
    )
    if r.status_code != 204:
        raise Exception(
            f"PUT request returned {r.status_code} code: expected 204\n{r}"
        )


def api_delete(api_route: str, reason: str = "") -> None:
    """Deletes an object from the api

    Args:
        api_route (str): The api route to delete the object from
        reason (str, optional): The reason of the action. Defaults to "".
    """
    r = requests.delete(
        url=f"{DISCORD_API}{api_route}",
        headers={"Authorization": f"Bot {KEPY_TOKEN}", "X-Audit-Log-Reason": reason},
    )
    if r.status_code != 204:
        raise Exception(
            f"DELETE request returned {r.status_code} code: expected 204\n{r}"
        )


def api_get_user(user_id) -> dict:
    """Gets an user from the api

    Args:
        user_id (int): The id of the user to retrieve

    Returns:
        dict: The user object
    """
    return api_get(api_route=f"/users/{user_id}")


def api_get_member(guild_id, member_id) -> dict:
    """Gets an user from the api

    Args:
        user_id (int): The id of the user to retrieve

    Returns:
        dict: The user object
    """
    return api_get(api_route=f"/guilds/{guild_id}/members/{member_id}")
