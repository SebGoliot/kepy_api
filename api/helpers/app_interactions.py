
def get_app_message(body):
    target = body["data"]["target_id"]
    return body["data"]["resolved"]["messages"][target]

def get_app_message_author(body):
    msg = get_app_message(body)
    return msg["author"]

def get_app_message_author_id(body):
    author = get_app_message_author(body)
    return author["id"]

def get_app_message_author_name(body):
    author = get_app_message_author(body)
    return author["username"]
