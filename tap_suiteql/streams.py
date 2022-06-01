"""Stream type classes for tap-suiteql."""

from singer_sdk import typing as th

from tap_suiteql.client import suiteqlStream


def schema_builder(attributes: set[str]) -> dict:
    property_list = th.PropertiesList()

    for attribute in attributes:
        property_list.append(th.Property(attribute, th.StringType))

    return property_list.to_dict()


class SubscriptionStream(suiteqlStream):
    name = "Subscription"
    path = "/query/v1/suiteql"
    # Always sort the replication key and format the replication_key
    body_query = (
        "select * "
        ",TO_CHAR(lastmodifieddate, 'YYYY-MM-DD HH:MI:SS') as lastmodifieddatetime "
        "from subscription "
        "order by TO_CHAR(lastmodifieddate, 'YYYY-MM-DD HH:MI:SS') ASC"
    )
    primary_keys = ["id"]
    replication_key = "lastmodifieddatetime"
