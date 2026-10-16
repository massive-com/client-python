import logging
import os
from typing import Optional

import certifi


def ca_bundle_path(logger: Optional[logging.Logger] = None) -> str:
    """
    Path of the CA bundle used to verify TLS connections.

    Honors the standard ``SSL_CERT_FILE`` and ``REQUESTS_CA_BUNDLE`` environment
    variables (used for example behind corporate TLS inspection), falling back to
    the certifi bundle. A variable that doesn't point to an existing file is
    skipped with a warning, so a stale value doesn't break connections.
    """
    for env_var in ("SSL_CERT_FILE", "REQUESTS_CA_BUNDLE"):
        path = os.environ.get(env_var)
        if not path:
            continue
        if os.path.isfile(path):
            return path
        if logger:
            logger.warning(
                "%s is set to %r, which isn't a file; ignoring it", env_var, path
            )
    return certifi.where()
