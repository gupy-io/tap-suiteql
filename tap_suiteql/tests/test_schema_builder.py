from singer_sdk import typing as th

from tap_suiteql.schema_builder import SchemaBuilder


class DummyStream:
    schema = {"type": "object", "properties": {}}

    def __init__(self, default_schema=False):
        if default_schema:
            self.schema = th.PropertiesList(
                th.Property("catalogtype", th.StringType),
                th.Property("chargetype", th.StringType),
                th.Property("enddate", th.StringType),
                th.Property("frequency", th.StringType),
                th.Property("id", th.StringType),
                th.Property("item", th.StringType),
                th.Property("linenumber", th.StringType),
                th.Property("priceplan", th.StringType),
                th.Property("prorateby", th.StringType),
                th.Property("proratebyoption", th.StringType),
                th.Property("quantity", th.StringType),
                th.Property("recurringamount", th.StringType),
                th.Property("repeatevery", th.StringType),
                th.Property("startdate", th.StringType),
                th.Property("startoffsetvalue", th.StringType),
                th.Property("status", th.StringType),
                th.Property("subscription", th.StringType),
            ).to_dict()

    replication_key = "somekey"

    def get_metadata(self):
        return {
            "x-ns-filterable": [
                "custbody_o2s_transaction_t_nr_seq_ad",
                "custbody_o2s_transaction_d_contingenci",
                "custbody_o2s_transaction_c_outra_reten",
                "custbody_o2s_to_subsidiary_t_logradour",
                "renewalNumber",
            ]
        }


def test_schema_definition():
    expected = th.PropertiesList(
        th.Property("custbody_o2s_transaction_t_nr_seq_ad", th.StringType),
        th.Property("custbody_o2s_transaction_d_contingenci", th.StringType),
        th.Property("custbody_o2s_transaction_c_outra_reten", th.StringType),
        th.Property("custbody_o2s_to_subsidiary_t_logradour", th.StringType),
        th.Property("renewalnumber", th.StringType),
        th.Property("somekey", th.DateTimeType),
    ).to_dict()

    schema = SchemaBuilder(DummyStream()).schema()

    assert expected == schema


def test_get_default_schema():
    expected = th.PropertiesList(
        th.Property("catalogtype", th.StringType),
        th.Property("chargetype", th.StringType),
        th.Property("enddate", th.StringType),
        th.Property("frequency", th.StringType),
        th.Property("id", th.StringType),
        th.Property("item", th.StringType),
        th.Property("linenumber", th.StringType),
        th.Property("priceplan", th.StringType),
        th.Property("prorateby", th.StringType),
        th.Property("proratebyoption", th.StringType),
        th.Property("quantity", th.StringType),
        th.Property("recurringamount", th.StringType),
        th.Property("repeatevery", th.StringType),
        th.Property("startdate", th.StringType),
        th.Property("startoffsetvalue", th.StringType),
        th.Property("status", th.StringType),
        th.Property("subscription", th.StringType),
    ).to_dict()

    schema = SchemaBuilder(DummyStream(default_schema=True)).schema()
    assert expected == schema, "SchemaBuilder should return the default schema"
