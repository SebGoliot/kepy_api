
def get_slash_options(body):
    data = body["data"]["options"]
    options = {}
    for opt in data:
        options |= {opt["name"]: opt["value"]}
    return options
