
def get_interaction_name(body: dict) -> str:
    """Get the name of the interaction"""
    return str(body["data"]["name"])


def get_interaction_guild_id(body: dict) -> int:
    """Get the guild id of the interaction"""
    return int(body["guild_id"])


def get_interaction_author_id(body: dict) -> int:
    """Get the author id of the interaction"""
    return int(body["member"]["user"]["id"])


def get_interaction_author_permissions(body: dict) -> int:
    """Get the author permissions of the interaction"""
    return int(body["member"]["permissions"])
