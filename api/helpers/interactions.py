
def get_interaction_name(body):
    return body["data"]["name"]

def get_interaction_guild_id(body):
    return body["guild_id"]

def get_interaction_author_id(body):
    return body["member"]["user"]["id"]

def get_interaction_author_permissions(body) -> int:
    return int(body["member"]["permissions"])
