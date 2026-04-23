class AuthError(Exception):
    """
    Empty or invalid API key
    """

    pass


class BadResponse(Exception):
    """
    Non-200 response from API
    """

    pass
