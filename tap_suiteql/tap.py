"""suiteql tap class."""
import json
import os
from typing import Any, List

from singer_sdk import Tap
from singer_sdk import typing as th

from tap_suiteql.query_builder import QueryBuilder  # JSON schema typing helpers
from tap_suiteql.schema_builder import SchemaBuilder
from tap_suiteql.streams import (
    # ChangeOrderLineStream,
    ChargeStream,
    # CustomerPaymentStream,
    # CustomerStream,
    # CustomlistGpyCompanysizeStream,
    # CustomlistGpyReadjustmentindexStream,
    # CustomrecordGpyStatuschangeOrderStream,
    # InvoiceStream,
    # ItemStream,
    # MonthlyRecurringRevenueStream,
    # SubscriptionChangeOrderStream,
    # SubscriptionLineStream,
    # SubscriptionPlanStream,
    # SubscriptionPriceIntervalStream,
    # SubscriptionStream,
)

STREAM_TYPES = {
    # "Subscription": SubscriptionStream,
    # "Customer": CustomerStream,
    # "Invoice": InvoiceStream,
    # "SubscriptionLine": SubscriptionLineStream,
    # "SubscriptionPriceInterval": SubscriptionPriceIntervalStream,
    # "SubscriptionPlan": SubscriptionPlanStream,
    # "ChangeOrderLine": ChangeOrderLineStream,
    "Charge": ChargeStream,
    # "CustomerPayment": CustomerPaymentStream,
    # "CustomlistGpyCompanysize": CustomlistGpyCompanysizeStream,
    # "CustomlistGpyReadjustmentindex": CustomlistGpyReadjustmentindexStream,
    # "CustomrecordGpyStatuschangeOrder": CustomrecordGpyStatuschangeOrderStream,
    # "SubscriptionChangeOrder": SubscriptionChangeOrderStream,
    # "Item": ItemStream,
    # "MonthlyRecurringRevenue": MonthlyRecurringRevenueStream,
}


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

    def get_stream_types(self) -> List[Any]:

        stream_types: Any = []
        select_statement = json.loads(os.environ.get("TAP_SUITEQL__SELECT", '["*.*"]'))

        if select_statement == ["*.*"]:
            stream_types = STREAM_TYPES.values()
        else:
            stream_types = [
                STREAM_TYPES.get(s.replace(".*", "")) for s in select_statement
            ]

        return stream_types

    def discover_streams(self) -> List[Any]:
        """Return a list of discovered streams."""

        stream_classes: List[Any] = []

        for stream_class in self.get_stream_types():
            schema = SchemaBuilder(stream_class(tap=self)).schema()
            body_query = QueryBuilder(stream_class(tap=self, schema=schema)).query()

            stream_classes.append(
                stream_class(tap=self, schema=schema, body_query=body_query)
            )

        return stream_classes
