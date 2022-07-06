from singer_sdk import typing as th

from tap_suiteql.client import suiteqlStream


class SchemaBuilder:
    def __init__(self, stream: suiteqlStream):
        self.stream: suiteqlStream = stream

    def _schema_builder(self, attributes: dict) -> dict:
        property_list = th.PropertiesList()
        if self.stream.replication_key:
            attributes.update({self.stream.replication_key: "date"})

        if self.stream.primary_keys:
            for key in self.stream.primary_keys:
                attributes.update({key: None})

        for attribute_name, attribute_type in attributes.items():
            if attribute_type == "date":
                property_list.append(
                    th.Property(attribute_name.lower(), th.DateTimeType)
                )
            else:
                property_list.append(th.Property(attribute_name.lower(), th.StringType))

        return property_list.to_dict()

    def schema(self):
        if self.stream.schema["properties"] == {}:
            record = self.stream.get_metadata()
            attributes = [
                r
                for r in record["x-ns-filterable"]
                if r not in self.stream.skip_attributes
            ]
            attributes_dict = {
                a: record["properties"][a].get("format") for a in attributes
            }
            return self._schema_builder(attributes_dict)
        else:
            return self.stream.schema
