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


class ResponseDecodeError(Exception):
    """
    Response body could not be decoded as JSON, e.g. a truncated payload.

    Only raised when the client is constructed with raise_on_decode_error=True; the default
    remains logging the error and returning an empty result.
    """

    pass
