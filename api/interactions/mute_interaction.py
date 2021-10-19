
from discord_perm.discord_perm_const import MANAGE_MESSAGES
from discord_perm.discord_perm import has_permission

from api.helpers.interactions import (
    get_interaction_author_id,
    get_interaction_author_permissions,
    get_interaction_guild_id,
)
from api.helpers.app_interactions import get_app_message_author
from api.helpers.mute import create_mute


def mute_author(body) -> str:
    """This function handles the mute app interaction and returns a message

    Args:
        body (dict): The interaction request body

    Returns:
        str: The returned message
    """

    if has_permission(get_interaction_author_permissions(body), MANAGE_MESSAGES):
        muted = get_app_message_author(body)
        create_mute(
            guild_id=get_interaction_guild_id(body),
            author_id=get_interaction_author_id(body),
            muted_id=muted["id"],
            duration=30 * 60,
            reason="Muted with application command",
        )
        return _mute_success(muted["username"], 30, True)
    return _mute_success("", 30, False)


def _mute_success(muted_name: str, duration: int, success: bool):
    if success:
        return f"{muted_name} has been muted for {duration} minutes."
    return "Seems like you are not allowed to do this.."
