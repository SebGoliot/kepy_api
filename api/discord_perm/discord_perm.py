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

    # if the member is the owner -> return administrator permission
    if member['user']['id'] == guild['owner_id']:
        return ADMINISTRATOR

    # get @everyone role as base permission
    permissions = 0
    for role in guild['roles']:
        if role['id'] == guild['id']:
            permissions = int(role['permissions'])
            break

    # get member base roles permissions
    for member_role in member['roles']:
        for guild_role in guild['roles']:
            if guild_role['id'] == member_role:
                permissions |= int(guild_role['permissions'])

    # if admin -> return admin
    if permissions & ADMINISTRATOR == ADMINISTRATOR:
        return ADMINISTRATOR

    return permissions


def get_overwrites(
    base_permissions:int, guild_id:int, member:dict, channel:dict 
    ) -> int:
 
    return 0
