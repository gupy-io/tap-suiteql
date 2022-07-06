from typing import List
from tap_suiteql.client import suiteqlStream


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
