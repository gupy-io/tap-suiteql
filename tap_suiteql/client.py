"""REST client handling, including suiteqlStream base class."""

import logging
import re
from typing import Any, Dict, Optional, cast, List
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
    stream_type = ""

    @property
    def url_base(self) -> str:
        return self.config["base_url"]

    records_jsonpath = "$.items[*]"

    next_page_token_jsonpath = "$.links[?(@.rel == 'next')].href"

    body_query = ""
    metadata_path = ""
    skip_attributes = []

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
        start_date = self.config.get("start_date")
        bookmark_date = self.get_starting_timestamp(context)
        current_body = QueryBuilder(self).query()

        if bookmark_date:
            start_date = bookmark_date.strftime("%Y-%m-%dT%H:%M:%S")

        if self.replication_key:
            replication_key_param = f":{self.replication_key}"
            current_body = current_body.replace(
                replication_key_param, f"'{start_date}'"
            )
        logging.warning(f"current_body: {current_body}")
        return {"q": current_body}

    def post_process(self, row: dict, context: Optional[dict] = None) -> dict:
        """As needed, append or transform raw data to match expected structure.
        Args:
            row: required - the record for processing.
            context: optional - the singer context object.
        Returns:
              A record that has been processed.
        """

        return row


class QueryBuilder:
    SELECT_STATEMENT = "select "
    WHERE_STATEMENT = "where "

    def __init__(self, stream: suiteqlStream):
        self.stream: suiteqlStream = stream

    def _get_column_select(self, schema: dict) -> List:
        column_select = []
        for attribute_name, properties in schema["properties"].items():
            if properties.get("format") == "date-time":
                column_select.append(
                    f"""TO_CHAR({attribute_name}, 'YYYY-MM-DD\"T\"HH24:MI:SS') {attribute_name}"""
                )
            else:
                column_select.append(attribute_name)
        return column_select

    def _query_builder(
        self, schema: dict, replication_key: str, entity_name: str, stream_type: str
    ) -> str:
        from_statement = f"from {entity_name}"
        where_clauses = ["1=1"]
        column_select = self._get_column_select(schema)
        if replication_key:
            where_clauses.append(
                f"{replication_key} >= TO_DATE(:{replication_key}, 'YYYY-MM-DD\"T\"HH24:MI:SS')"
            )
        if stream_type:
            from_statement = f"from transaction"
            where_clauses.append(f"type = '{stream_type}'")
        self.SELECT_STATEMENT += ",".join(column_select)
        self.WHERE_STATEMENT += " and ".join(where_clauses)
        query = (
            f"{self.SELECT_STATEMENT} {from_statement} {self.WHERE_STATEMENT}".strip()
        )
        return query

    def query(self):
        return self._query_builder(
            self.stream.schema,
            self.stream.replication_key,
            self.stream.name,
            self.stream.stream_type,
        )
