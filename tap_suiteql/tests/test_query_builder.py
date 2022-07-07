from tap_suiteql.query_builder import QueryBuilder


class DummyStream:
    name = "dummy"
    entity_name = ""
    replication_key = "replication_key_col"
    skip_attributes = []
    stream_type = None
    schema = {
        "type": "object",
        "properties": {
            "col_1": {},
            "col_2": {},
            "date_col": {"format": "date-time"},
            "replication_key_col": {"format": "date-time"},
        },
    }


class DummyStreamWithoutReplicationKey:
    name = "dummy_without_replication_key"
    entity_name = ""
    skip_attributes = []
    replication_key = None
    stream_type = None
    schema = {
        "type": "object",
        "properties": {
            "col_1": {},
            "col_2": {},
            "date_col": {"format": "date-time"},
        },
    }


class DummyStreamTransaction:
    name = "dummy"
    entity_name = "dummy_transaction"
    replication_key = "replication_key_col"
    stream_type = "CustDummy"
    skip_attributes = []
    schema = {
        "type": "object",
        "properties": {
            "col_1": {},
            "col_2": {},
            "date_col": {"format": "date-time"},
            "replication_key_col": {"format": "date-time"},
        },
    }


def test_sql_builder_with_replication_key():
    expected = """select col_1,col_2,TO_CHAR(date_col, 'YYYY-MM-DD\"T\"HH24:MI:SS') date_col,TO_CHAR(replication_key_col, 'YYYY-MM-DD\"T\"HH24:MI:SS') replication_key_col from dummy where 1=1 and replication_key_col >= TO_DATE(:replication_key_col, 'YYYY-MM-DD\"T\"HH24:MI:SS')"""  # noqa:E501
    query = QueryBuilder(DummyStream).query()

    assert expected == query


def test_sql_builder_without_replication_key():
    expected = """select col_1,col_2,TO_CHAR(date_col, 'YYYY-MM-DD\"T\"HH24:MI:SS') date_col from dummy_without_replication_key where 1=1"""  # noqa:E501
    query = QueryBuilder(DummyStreamWithoutReplicationKey).query()

    assert expected == query


def test_sql_builder_from_transaction():
    expected = """select col_1,col_2,TO_CHAR(date_col, 'YYYY-MM-DD\"T\"HH24:MI:SS') date_col,TO_CHAR(replication_key_col, 'YYYY-MM-DD\"T\"HH24:MI:SS') replication_key_col from dummy_transaction where 1=1 and replication_key_col >= TO_DATE(:replication_key_col, 'YYYY-MM-DD\"T\"HH24:MI:SS') and type = 'CustDummy'"""  # noqa:E501
    query = QueryBuilder(DummyStreamTransaction).query()

    assert expected == query
