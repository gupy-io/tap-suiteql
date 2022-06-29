"""suiteql tap class."""

from typing import List

from singer_sdk import Stream, Tap
from singer_sdk import typing as th  # JSON schema typing helpers

from tap_suiteql.schema_builder import SchemaBuilder
from tap_suiteql.streams import (
    CustomerStream,
    InvoiceStream,
    SubscriptionLineStream,
    SubscriptionStream,
    SubscriptionPriceIntervalStream,
    SubscriptionPlanStream,
    ChangeOrderLineStream,
    CustomlistGpyCompanysizeStream,
)

STREAM_TYPES = [
    SubscriptionStream,
    CustomerStream,
    InvoiceStream,
    SubscriptionLineStream,
    SubscriptionPriceIntervalStream,
    SubscriptionPlanStream,
    ChangeOrderLineStream
    CustomlistGpyCompanysizeStream,
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

            stream_classes.append(stream_class(tap=self, schema=schema))

        return stream_classes
