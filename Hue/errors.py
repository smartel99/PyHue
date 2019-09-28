class HTTPException(Exception):
    def __init__(self, error_code):
        self.msg = f"HTTPException: Request returned {error_code}."


class InvalidRequest(Exception):
    def __init__(self, resp):
        if type(resp) == list:
            resp = resp[0]
        self.msg = f"InvalidRequest:\n\tError Code: {resp['error']['type']}\n\t" \
                   f"URL: \"{resp['error']['address']}\n\t" \
                   f"Description: {resp['error']['description']}"


class InvalidArgument(Exception):
    def __init__(self, arg_type, arg_val):
        self.msg = f"Invalid Argument: \"{arg_val}\" is not a \"{arg_type}\""
