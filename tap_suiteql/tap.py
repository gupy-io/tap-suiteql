"""suiteql tap class."""

from typing import List

from singer_sdk import Stream, Tap
from singer_sdk import typing as th

from tap_suiteql.query_builder import QueryBuilder  # JSON schema typing helpers
from tap_suiteql.schema_builder import SchemaBuilder
from tap_suiteql.streams import (
    ChangeOrderLineStream,
    CustomerPaymentStream,
    CustomerStream,
    CustomlistGpyCompanysizeStream,
    CustomlistGpyReadjustmentindexStream,
    InvoiceStream,
    SubscriptionLineStream,
    SubscriptionPlanStream,
    SubscriptionPriceIntervalStream,
    SubscriptionStream,
)

STREAM_TYPES = [
    SubscriptionStream,
    CustomerStream,
    InvoiceStream,
    SubscriptionLineStream,
    SubscriptionPriceIntervalStream,
    SubscriptionPlanStream,
    ChangeOrderLineStream,
    CustomerPaymentStream,
    CustomlistGpyCompanysizeStream,
    CustomlistGpyReadjustmentindexStream,
]


class Tapsuiteql(Tap):
    """suiteql tap class."""

    name = "tap-suiteql"

    config_jsonschema = th.PropertiesList(
        th.Property(
            "start_date",
            th.StringType,
            required=True,
        ),
        th.Property(
            "consumer_secret",
            th.StringType,
            required=True,
        ),
        th.Property(
            "consumer_key",
            th.StringType,
            required=True,
        ),
        th.Property(
            "token_id",
            th.StringType,
            required=True,
        ),
        th.Property(
            "token_secret",
            th.StringType,
            required=True,
        ),
        th.Property(
            "account_id",
            th.StringType,
            required=True,
        ),
        th.Property(
            "base_url",
            th.StringType,
            description="The url for the API service",
            required=True,
        ),
    ).to_dict()

    def discover_streams(self) -> List[Stream]:
        """Return a list of discovered streams."""

        stream_classes: List[Stream] = []

        for stream_class in STREAM_TYPES:
            schema = SchemaBuilder(stream_class(tap=self)).schema()
            body_query = QueryBuilder(stream_class(tap=self, schema=schema)).query()

            stream_classes.append(
                stream_class(tap=self, schema=schema, body_query=body_query)
            )

        return stream_classes
