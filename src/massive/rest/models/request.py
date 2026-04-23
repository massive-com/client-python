from typing import Dict, Optional

X_MASSIVE_EDGE_ID = "X-Massive-Edge-ID"
X_MASSIVE_EDGE_IP_ADDRESS = "X-Massive-Edge-IP-Address"
X_MASSIVE_EDGE_USER_AGENT = "X-Massive-Edge-User-Agent"

HEADER = "header"


class RequestOptionBuilder:
    def __init__(
        self,
        edge_id: Optional[str] = None,
        edge_ip_address: Optional[str] = None,
        edge_user: Optional[str] = None,
    ):
        """
        RequestOptionBuilder is a utility class to build massive api options used in requests.
        :param edge_id: is a required Launchpad header. It identifies the Edge User requesting data
        :param edge_ip_address: is a required Launchpad header. It denotes the originating IP Address of the Edge User
        :param edge_user: is an optional Launchpad header. It denotes the originating UserAgent of the Edge User requesting data.
        """
        self.headers: Optional[Dict[str, str]] = None
        if edge_id is not None and edge_ip_address is not None:
            self.edge_headers(
                edge_id=edge_id, edge_ip_address=edge_ip_address, edge_user=edge_user
            )

    def edge_headers(
        self,
        edge_id: str,
        edge_ip_address: str,
        edge_user: Optional[str] = None,
    ) -> "RequestOptionBuilder":
        """
        require_edge_headers adds required headers to the headers' dictionary
        :param edge_id: is a required Launchpad header. It identifies the Edge User requesting data
        :param edge_ip_address: is a required Launchpad header. It denotes the originating IP Address of the Edge User
        requesting data
        :param edge_user: user_agent: is an optional Launchpad header. It denotes the originating UserAgent of the Edge
        User requesting data
        :return ResponseOptionBuilder
        """
        edge_headers: Dict[str, str] = {
            X_MASSIVE_EDGE_ID: edge_id,
            X_MASSIVE_EDGE_IP_ADDRESS: edge_ip_address,
        }

        if edge_user is not None:
            edge_headers[X_MASSIVE_EDGE_USER_AGENT] = edge_user

        self._add_to_edge_headers(**edge_headers)

        return self

    def update_edge_header(
        self,
        edge_id: Optional[str] = None,
        edge_ip_address: Optional[str] = None,
        edge_user: Optional[str] = None,
    ) -> "RequestOptionBuilder":
        """
        used to change individual edge elements of underlying headers' dictionary.
        :param edge_id: is a required Launchpad header. It identifies the Edge User requesting data
        :param edge_ip_address: is a required Launchpad header. It denotes the originating IP Address of the Edge User
        requesting data
        :param edge_user: user_agent: is an optional Launchpad header. It denotes the originating UserAgent of the Edge
        User requesting data
        :return:
        """
        if self.headers is None:
            raise RequestOptionError(
                "must set required fields prior to using update function."
            )
        edge_headers: Dict[str, str] = {}

        if edge_id is not None:
            edge_headers[X_MASSIVE_EDGE_ID] = edge_id

        if edge_ip_address is not None:
            edge_headers[X_MASSIVE_EDGE_IP_ADDRESS] = edge_ip_address

        if edge_user is not None:
            edge_headers[X_MASSIVE_EDGE_USER_AGENT] = edge_user

        self._add_to_edge_headers(**edge_headers)

        return self

    def _add_to_edge_headers(self, **headers):
        if self.headers is None:
            self.headers = {}

        for k, v in headers.items():
            self.headers[k] = v


class RequestOptionError(Exception):
    """
    Missing required option.
    """
