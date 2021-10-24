from datetime import datetime, timezone

from kepy.settings.base import DISCORD_CDN
from api.models import DiscordUser, Guild, Member


def get_guild_by_id(guild_id) -> Guild:
    """Get a Guild by id

    Args:
        guild_id (int): The id of the guild to get

    Returns:
        Guild: The Guild
    """
    return Guild.objects.get_or_create(
        id=guild_id,
        date_created=get_snowflake_time(guild_id),
    )[0]


def get_user_by_id(user_id) -> DiscordUser:
    """Get a DiscordUser by id

    Args:
        user_id (int): The id of the user to get

    Returns:
        DiscordUser: The DiscordUser
    """
    return DiscordUser.objects.get_or_create(id=user_id)[0]


def get_member_by_id(guild_id, member_id) -> Member:
    """Get a DiscordUser by id

    Args:
        user_id (int): The id of the user to get

    Returns:
        DiscordUser: The DiscordUser
    """
    user = get_user_by_id(user_id=member_id)
    guild = get_guild_by_id(guild_id=guild_id)
    return Member.objects.get_or_create(user=user, guild=guild)[0]


def get_snowflake_time(snowflake) -> datetime:
    """Gets a datetime from a Discord snowflake

    Args:
        snowflake (int): The snowflake to get time from

    Returns:
        Datetime: The datetime from the snowflake
    """
    timestamp = ((int(snowflake) >> 22) + 1420070400000) / 1000
    return datetime.utcfromtimestamp(timestamp).replace(tzinfo=timezone.utc)


def get_avatar_url(user_id, avatar) -> str:
    """Returns the avatar url from the user id and avatar id

    Args:
        user_id (int): The user id
        avatar (str): The avatar id

    Returns:
        str: The avatar URL
    """
    return f"{DISCORD_CDN}/avatars/{user_id}/{avatar}"
