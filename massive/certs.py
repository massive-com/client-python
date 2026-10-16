import os
import certifi


def ca_bundle_path() -> str:
    """
    Path of the CA bundle used to verify TLS connections.

    Honors the standard ``SSL_CERT_FILE`` and ``REQUESTS_CA_BUNDLE`` environment
    variables (used for example behind corporate TLS inspection), falling back to
    the certifi bundle.
    """
    return (
        os.environ.get("SSL_CERT_FILE")
        or os.environ.get("REQUESTS_CA_BUNDLE")
        or certifi.where()
    )
