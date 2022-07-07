from typing import List

from tap_suiteql.client import suiteqlStream


class QueryBuilder:
    def __init__(self, stream: suiteqlStream):
        self.stream: suiteqlStream = stream

    def _get_column_select(self, schema: dict) -> List:
        column_select = []
        for attribute_name, properties in schema["properties"].items():
            if properties.get("format") == "date-time":
                column_select.append(
                    f"""TO_CHAR({attribute_name}, 'YYYY-MM-DD\"T\"HH24:MI:SS') {attribute_name}"""  # noqa
                )
            else:
                column_select.append(attribute_name)
        return column_select

    def _build_select_statement(self, stream: suiteqlStream) -> str:
        select_statement = "select "
        column_select = self._get_column_select(stream.schema)
        select_statement += ",".join(column_select)
        return select_statement

    def _build_from_statement(self, stream: suiteqlStream):
        if stream.entity_name:
            return f"from {stream.entity_name}"
        else:
            return f"from {stream.name}"

    def _build_where_statement(self, stream: suiteqlStream):
        where_clauses = ["1=1"]
        where_statement = "where "
        if stream.replication_key:
            where_clauses.append(
                f"{stream.replication_key} >= TO_DATE(:{stream.replication_key}, 'YYYY-MM-DD\"T\"HH24:MI:SS')"  # noqa
            )
        if stream.stream_type:
            where_clauses.append(f"type = '{stream.stream_type}'")
        where_statement += " and ".join(where_clauses)
        return where_statement

    def _query_builder(self, stream: suiteqlStream) -> str:
        select_statement = self._build_select_statement(stream)
        from_statement = self._build_from_statement(stream)
        where_statement = self._build_where_statement(stream)
        query = f"{select_statement} {from_statement} {where_statement}".strip()
        return query

    def query(self):
        return self._query_builder(self.stream)
