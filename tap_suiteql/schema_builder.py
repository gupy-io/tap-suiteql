from singer_sdk import typing as th

from tap_suiteql.client import suiteqlStream


class SchemaBuilder:
    def __init__(self, stream: suiteqlStream):
        self.stream: suiteqlStream = stream

    def _schema_builder(self, attributes: dict) -> dict:
        property_list = th.PropertiesList()
        if self.stream.replication_key:
            attributes.update({self.stream.replication_key: "date"})

        for attribute_name, attribute_type in attributes.items():
            if attribute_name != "links":
                if attribute_type == "date":
                    property_list.append(
                        th.Property(attribute_name.lower(), th.DateTimeType)
                    )
                else:
                    property_list.append(
                        th.Property(attribute_name.lower(), th.StringType)
                    )

        return property_list.to_dict()

    def schema(self):
        if self.stream.schema["properties"] == {}:
            record = self.stream.get_metadata()
            attributes = record["x-ns-filterable"]
            attributes_dict = {
                a: record["properties"][a].get("format") for a in attributes
            }
            return self._schema_builder(attributes_dict)
        else:
            return self.stream.schema
