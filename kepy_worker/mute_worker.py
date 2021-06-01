from api.helpers.mute import end_member_mutes
from kepy.discord_api_shortcuts import api_put, api_delete
from kepy_worker import app


@app.task
def mute(guild_id: int, user_id: int, mute_role_id: int, reason: str) -> None:
    """This function handles the muting of members

    Args:
        guild_id (int): the guild id of the member
        user_id (int): the user id of the member
        mute_role_id (int): the id of the mute role
        mute_time (int): the duration of the mute, sets the unmute task
        author (str): the name of the mute author
        reason (str): the reason of the mute
    """

    api_route = f"/guilds/{guild_id}/members/{user_id}/roles/{mute_role_id}"
    api_put(api_route, reason)
    # TODO: handle request errors (404, etc..)


@app.task
def unmute(guild_id: int, user_id: int, mute_role_id: int, reason: str) -> None:
    """This function handles the unmutting of the members

    Args:
        guild_id (int): the guild id of the member
        user_id (int): the user id of the member
        mute_role_id (int): the id of the mute role
        reason (str): the reason of the unmute
    """

    end_member_mutes(guild_id, user_id)

    api_route = f"/guilds/{guild_id}/members/{user_id}/roles/{mute_role_id}"
    api_delete(api_route, reason)
    # TODO: handle request errors (404, etc..)
