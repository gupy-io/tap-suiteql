from tap_suiteql.client import suiteqlStream
from singer_sdk import typing as th


class QueryBuilder:
    def __init__(self, stream: suiteqlStream):
        self.stream: suiteqlStream = stream

    def _query_builder(
        self, schema: dict, replication_key: str, entity_name: str
    ) -> str:
        select_statement = "select "
        from_statement = f"from {entity_name}"
        where_statement = "where "
        column_select = []
        where_clauses = ["1=1"]
        for attribute_name, properties in schema["properties"].items():
            if properties.get("format") == "date-time":
                column_select.append(
                    f"""TO_CHAR({attribute_name}, 'YYYY-MM-DD\"T\"HH24:MI:SSTZH:TZM') {attribute_name}"""
                )
            else:
                column_select.append(attribute_name)
        if replication_key:
            where_clauses.append(
                f"{replication_key} >= TO_DATE(:lastmodifieddatetime, 'YYYY-MM-DD\"T\"HH24:MI:SS')"
            )
        select_statement += ",".join(column_select)
        where_statement += " and ".join(where_clauses)
        query = f"{select_statement} {from_statement} {where_statement}".strip()
        return query

    def query(self):
        return self._query_builder(
            self.stream.schema, self.stream.replication_key, self.stream.name
        )
