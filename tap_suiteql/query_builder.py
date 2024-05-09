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
                    f"""TO_CHAR({attribute_name}, 'YYYY-MM-DD\"T\"HH24:MI:SS') {attribute_name}"""  # noqa:E501
                )
            else:
                column_select.append(attribute_name)

        return column_select

    def _build_select_statement(self) -> str:
        select_statement = "select "
        column_select = self._get_column_select(self.stream.schema)
        select_statement += ",".join(column_select)

        return select_statement

    def _build_from_statement(self):
        if self.stream.entity_name:
            return f"from {self.stream.entity_name}"
        else:
            return f"from {self.stream.name}"

    def _build_where_statement(self):
        where_clauses = ["1=1"]
        where_statement = "where "

        if (
            self.stream.year_date_field
        ):  # Filter added due to the limit of 100 thousand records that the Sensedata API returns # noqa:E501
            where_clauses.append(
                f"TO_CHAR({self.stream.year_date_field}, 'YYYY') >= 2024 and {self.stream.year_date_field} < ADD_MONTHS(SYSDATE, 3)"  # noqa:E501
            )

        if self.stream.replication_key:
            where_clauses.append(
                f"{self.stream.replication_key} >= TO_DATE(:{self.stream.replication_key}, 'YYYY-MM-DD\"T\"HH24:MI:SS')"  # noqa:E501
            )

        if self.stream.stream_type:
            where_clauses.append(f"type = '{self.stream.stream_type}'")

        where_statement += " and ".join(where_clauses)
        return where_statement

    def _build_order_statement(self):
        order_statement = None

        if self.stream.replication_key and self.stream.primary_keys:
            order_statement = (
                f"order by {self.stream.replication_key},{self.stream.primary_keys[0]}"
            )
        elif self.stream.replication_key is None and self.stream.primary_keys:
            order_statement = f"order by {self.stream.primary_keys[0]}"
        return "" if order_statement is None else order_statement

    def query(self) -> str:
        select_statement = self._build_select_statement()
        from_statement = self._build_from_statement()
        where_statement = self._build_where_statement()
        order_statement = self._build_order_statement()

        query = f"""
            {select_statement}
            {from_statement}
            {where_statement}
            {order_statement}
        """.strip()

        return query
