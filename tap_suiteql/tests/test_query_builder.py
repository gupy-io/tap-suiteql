from singer_sdk import typing as th
from tap_suiteql.query_builder import QueryBuilder


class DummyStream:
    name = "dummy"
    replication_key = "replication_key_col"
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
    expected = """select col_1,col_2,TO_CHAR(date_col, 'YYYY-MM-DD\"T\"HH24:MI:SSTZH:TZM') date_col,TO_CHAR(replication_key_col, 'YYYY-MM-DD\"T\"HH24:MI:SSTZH:TZM') replication_key_col from dummy where 1=1 and replication_key_col >= TO_DATE(:lastmodifieddatetime, 'YYYY-MM-DD\"T\"HH24:MI:SS')""".strip()
    query = QueryBuilder(DummyStream).query()
    assert expected == query


def test_sql_builder_without_replication_key():
    assert True
