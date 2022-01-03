
def get_slash_options(body:dict) -> dict:
    """Get the options from a slash interaction

    Args:
        body (dict): The body of the slash interaction

    Returns:
        dict: The options of the interaction
    """
    options = {}
    for option in body["data"]["options"]:
        options |= {option["name"]: option["value"]}
    return options
