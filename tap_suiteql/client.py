"""REST client handling, including suiteqlStream base class."""

from typing import Any, Dict, Optional, cast
from urllib.parse import parse_qsl, urlparse

import backoff
import requests
from singer_sdk.streams import RESTStream

from tap_suiteql.auth import suiteqlAuthenticator


class suiteqlStream(RESTStream):
    """suiteql stream class."""

    def __init__(
        self, tap: Any, schema: dict = {"type": "object", "properties": {}}
    ) -> None:
        super().__init__(tap=tap, schema=schema)

    rest_method = "POST"

    @property
    def url_base(self) -> str:
        return self.config["base_url"]

    records_jsonpath = "$.items[*]"

    next_page_token_jsonpath = "$.links[?(@.rel == 'next')].href"

    body_query = ""
    metadata_path = ""

    @property
    def authenticator(self) -> suiteqlAuthenticator:
        """Return a new authenticator object."""
        return suiteqlAuthenticator.create_for_stream(self)

    @property
    def http_headers(self) -> dict:
        """Return the http headers needed."""
        headers = {}
        if "user_agent" in self.config:
            headers["User-Agent"] = self.config.get("user_agent")

        headers["prefer"] = "transient"
        headers["Cookie"] = "NS_ROUTING_VERSION=LAGGING"
        headers["Content-Type"] = "application/json"

        return headers

    def prepare_request(
        self, context: Optional[dict], next_page_token: Optional[Any]
    ) -> requests.PreparedRequest:
        http_method = self.rest_method

        url: str = self.get_url(context)
        params: dict = self.get_url_params(context, next_page_token)
        request_data = self.prepare_request_payload(context, next_page_token)
        headers = self.http_headers

        authenticator = self.authenticator

        if authenticator:
            auth = authenticator.oauth_object()

        request = cast(
            requests.PreparedRequest,
            self.requests_session.prepare_request(
                requests.Request(
                    method=http_method,
                    auth=auth,
                    url=url,
                    params=params,
                    headers=headers,
                    json=request_data,
                ),
            ),
        )
        return request

    def _get_metadata_url(self):
        if self.metadata_path == "":
            raise AttributeError("Invalid metadata path")

        return "".join([self.url_base, self.metadata_path or ""])

    @backoff.on_exception(
        backoff.expo, requests.exceptions.RequestException, max_time=300
    )
    def get_metadata(self):
        url: str = self._get_metadata_url()
        request_data = self.prepare_request_payload(None, "")
        headers = self.http_headers
        authenticator = self.authenticator

        headers["Accept"] = "application/schema+json"
        headers["Connection"] = "keep-alive"

        auth = authenticator.oauth_object()

        prepared_request = cast(
            requests.PreparedRequest,
            self.requests_session.prepare_request(
                requests.Request(
                    method="GET",
                    auth=auth,
                    url=url,
                    headers=headers,
                    json=request_data,
                ),
            ),
        )

        response = self.requests_session.send(prepared_request)

        return response.json()

    def get_url_params(
        self, context: Optional[dict], next_page_token: Optional[Any]
    ) -> Dict[str, Any]:
        """Return a dictionary of values to be used in URL parameterization."""
        params: dict = {}

        if next_page_token:
            next_page_url = urlparse(next_page_token)
            params = dict(parse_qsl(next_page_url.query))

        return params

    def prepare_request_payload(
        self, context: Optional[dict], next_page_token: Optional[Any]
    ) -> Optional[dict]:
        """Prepare the data payload for the REST API request.

        By default, no payload will be sent (return None).
        """

        return {"q": self.body_query}

    def post_process(self, row: dict, context: Optional[dict] = None) -> dict:
        """As needed, append or transform raw data to match expected structure.
        Args:
            row: required - the record for processing.
            context: optional - the singer context object.
        Returns:
              A record that has been processed.
        """

        return row
