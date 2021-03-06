from .discord_perm_const import *


def get_base_permissions(guild: dict, member: dict) -> int:
    """This function gets the base permissions of a guild, this is used to
    compute a member's base permission

    Args:
        guild (dict): The guild object
        member (dict): The member object

    Returns:
        int: The base permission value for this member based on his roles
    """

    # if the member is the owner -> return all permissions
    if member["user"]["id"] == guild["owner_id"]:
        return ALL_PERMISSIONS

    permissions = 0

    # get @everyone role as base permission
    for guild_role in guild["roles"]:
        if guild_role["id"] == guild["id"]:
            permissions = int(guild_role["permissions"])
            break

    # get member roles base permissions
    for member_role in member["roles"]:
        for guild_role in guild["roles"]:
            if guild_role["id"] == member_role:
                permissions |= int(guild_role["permissions"])

    # if admin -> return all permissions
    if permissions & ADMINISTRATOR == ADMINISTRATOR:
        return ALL_PERMISSIONS

    return permissions


def get_overwrites(
    base_permissions: int, guild_id: str, member: dict, channel: dict
) -> int:
    """
    This function gets the overwrites for a specific channel and member and
    returns the permissions for this member in this channel based on the base
    permissions of the guild and the overwrites of the channel and member in
    this channel

    Args:
        base_permissions (int): The base permissions of the guild
        guild_id (str): The guild id
        member (dict): The member object
        channel (dict): The channel object

    Returns:
        int: The permissions for this member in this channel
    """

    # if the member has administrator rights -> return all permissions
    if base_permissions & ADMINISTRATOR == ADMINISTRATOR:
        return ALL_PERMISSIONS

    overwrite_everyone = None
    permissions = base_permissions

    # get the everyone role overwrites
    for channel_perm_overwrites in channel["permission_overwrites"]:
        if channel_perm_overwrites["id"] == guild_id:
            overwrite_everyone = channel_perm_overwrites

    # add the everyone overwrites
    if overwrite_everyone != None:
        permissions &= ~int(overwrite_everyone["deny"])
        permissions |= int(overwrite_everyone["allow"])

    overwrites = channel["permission_overwrites"]
    allow, deny = EMPTY_PERMISSION, EMPTY_PERMISSION

    # add the member's roles overwrites
    for member_role_id in member["roles"]:
        for each in overwrites:
            if each["id"] == member_role_id:
                allow |= int(each["allow"])
                deny |= int(each["deny"])

    permissions &= ~deny
    permissions |= allow

    # get member specific overwrites
    for each in overwrites:
        if each["id"] == member["user"]["id"]:
            permissions &= ~int(each["deny"])
            permissions |= int(each["allow"])
            break

    return permissions


def check_permissions(
    guild: dict, member: dict, channel: dict, target_permission: int
) -> bool:
    """This function checks if the member has the target permission in the
    channel

    Args:
        guild (dict): The guild object
        member (dict): The member object
        channel (dict): The channel object
        target_permission (int): The permission to check

    Returns:
        bool: True if the member has the target permission in the channel
    """

    base_permissions = get_base_permissions(guild, member)
    overwrites = get_overwrites(base_permissions, guild["id"], member, channel)

    return has_permission(overwrites, target_permission)


def has_permission(member_permission: int, target_permission: int) -> bool:
    return member_permission & target_permission == target_permission
