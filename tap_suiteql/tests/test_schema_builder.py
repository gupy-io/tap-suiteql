from singer_sdk import typing as th

from tap_suiteql.schema_builder import SchemaBuilder


class DummyStream:

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
