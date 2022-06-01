from singer_sdk import typing as th

from tap_suiteql.client import suiteqlStream


class SchemaBuilder:
    def __init__(self, stream: suiteqlStream):
        self.stream: suiteqlStream = stream

    def _schema_builder(self, attributes: list[str]) -> dict:
        property_list = th.PropertiesList()

        for attribute in attributes:
            if attribute != "links":
                property_list.append(th.Property(attribute, th.StringType))

        return property_list.to_dict()

    def schema(self):
        record = self.stream.get_one_record()

        attributes = list(record["items"][0].keys())

        return self._schema_builder(attributes)
