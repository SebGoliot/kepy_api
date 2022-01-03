
def get_app_message(body):
    """Get the app message from a body"""
    target = body["data"]["target_id"]
    return body["data"]["resolved"]["messages"][target]

def get_app_message_author(body):
    """Get the author of the app message"""
    msg = get_app_message(body)
    return msg["author"]

def get_app_message_author_id(body):
    """Get the author id of the app message"""
    author = get_app_message_author(body)
    return author["id"]

def get_app_message_author_name(body):
    """Get the author name of the app message"""
    author = get_app_message_author(body)
    return author["username"]
