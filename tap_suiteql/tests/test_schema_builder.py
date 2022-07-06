from singer_sdk import typing as th

from tap_suiteql.schema_builder import SchemaBuilder


class DummyStream:
    schema = {"type": "object", "properties": {}}
    replication_key = "somekey"
    primary_keys = ["renewalNumber"]
    skip_attributes = []

    def get_metadata(self):
        return {
            "properties": {
                "custbody_o2s_transaction_t_nr_seq_ad": {"format": None},
                "custbody_o2s_transaction_d_contingenci": {"format": None},
                "custbody_o2s_transaction_c_outra_reten": {"format": "date"},
                "custbody_o2s_to_subsidiary_t_logradour": {"format": None},
                "renewalNumber": {"format": "int64"},
            },
            "x-ns-filterable": [
                "custbody_o2s_transaction_t_nr_seq_ad",
                "custbody_o2s_transaction_d_contingenci",
                "custbody_o2s_transaction_c_outra_reten",
                "custbody_o2s_to_subsidiary_t_logradour",
                "renewalNumber",
            ],
        }


class DummyStreamWithSchema:
    schema = th.PropertiesList(
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


class DummyStreamWithSkipAttribute:
    schema = {"type": "object", "properties": {}}
    replication_key = "somekey"
    primary_keys = ["renewalNumber"]
    skip_attributes = [
        "custbody_o2s_transaction_c_outra_reten",
        "custbody_o2s_to_subsidiary_t_logradour",
    ]

    def get_metadata(self):
        return {
            "properties": {
                "custbody_o2s_transaction_t_nr_seq_ad": {"format": None},
                "custbody_o2s_transaction_d_contingenci": {"format": None},
                "custbody_o2s_transaction_c_outra_reten": {"format": "date"},
                "custbody_o2s_to_subsidiary_t_logradour": {"format": None},
                "renewalNumber": {"format": "int64"},
            },
            "x-ns-filterable": [
                "custbody_o2s_transaction_t_nr_seq_ad",
                "custbody_o2s_transaction_d_contingenci",
                "custbody_o2s_transaction_c_outra_reten",
                "custbody_o2s_to_subsidiary_t_logradour",
                "renewalNumber",
            ],
        }


def test_schema_definition():
    expected = th.PropertiesList(
        th.Property("custbody_o2s_transaction_t_nr_seq_ad", th.StringType),
        th.Property("custbody_o2s_transaction_d_contingenci", th.StringType),
        th.Property("custbody_o2s_transaction_c_outra_reten", th.DateTimeType),
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

    schema = SchemaBuilder(DummyStreamWithSchema()).schema()
    assert expected == schema, "SchemaBuilder should return the default schema"


def test_skip_attributes():
    expected = th.PropertiesList(
        th.Property("custbody_o2s_transaction_t_nr_seq_ad", th.StringType),
        th.Property("custbody_o2s_transaction_d_contingenci", th.StringType),
        th.Property("renewalnumber", th.StringType),
        th.Property("somekey", th.DateTimeType),
    ).to_dict()
    schema = SchemaBuilder(DummyStreamWithSkipAttribute()).schema()
    assert expected == schema


def test_get_attributes_dict():
    expected = {
        "custbody_o2s_transaction_t_nr_seq_ad": None,
        "custbody_o2s_transaction_d_contingenci": None,
        "custbody_o2s_transaction_c_outra_reten": "date",
        "custbody_o2s_to_subsidiary_t_logradour": None,
        "renewalNumber": "int64",
    }
    attributes_dict = SchemaBuilder(DummyStream())._get_attributes_dict()
    assert attributes_dict == expected


def test_add_primary_keys_to_attributes_map():
    expected = {
        "custbody_o2s_transaction_t_nr_seq_ad": None,
        "custbody_o2s_transaction_d_contingenci": None,
        "custbody_o2s_transaction_c_outra_reten": "date",
        "custbody_o2s_to_subsidiary_t_logradour": None,
        "renewalNumber": None,
    }
    attributes_dict = SchemaBuilder(DummyStream())._get_attributes_dict()
    incremented_attributes_dict = SchemaBuilder(
        DummyStream()
    )._add_primary_keys_to_attributes_map(attributes_dict)
    assert expected == incremented_attributes_dict


def test_add_replication_key_to_attributes_map():
    expected = {
        "custbody_o2s_transaction_t_nr_seq_ad": None,
        "custbody_o2s_transaction_d_contingenci": None,
        "custbody_o2s_transaction_c_outra_reten": "date",
        "custbody_o2s_to_subsidiary_t_logradour": None,
        "renewalNumber": "int64",
        "somekey": "date",
    }
    attributes_dict = SchemaBuilder(DummyStream())._get_attributes_dict()
    incremented_attributes_dict = SchemaBuilder(
        DummyStream()
    )._add_replication_key_to_attributes_map(attributes_dict)
    assert expected == incremented_attributes_dict
