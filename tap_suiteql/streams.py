"""Stream type classes for tap-suiteql."""

from tap_suiteql.client import suiteqlStream
from singer_sdk import typing as th


class SubscriptionStream(suiteqlStream):
    name = "Subscription"
    path = "/query/v1/suiteql"
    metadata_path = "/record/v1/metadata-catalog/subscription"
    # Always sort the replication key and format the replication_key
    body_query = """
        select *
        ,TO_CHAR(lastmodifieddate, 'YYYY-MM-DD\"T\"HH24:MI:SSTZH:TZM') as lastmodifieddatetime
        FROM subscription
        order by lastmodifieddate ASC
        """
    primary_keys = ["id"]
    replication_key = "lastmodifieddatetime"


class CustomerStream(suiteqlStream):
    name = "Customer"
    path = "/query/v1/suiteql"
    metadata_path = "/record/v1/metadata-catalog/customer"
    # Always sort the replication key and format the replication_key
    body_query = """
        select *
        ,TO_CHAR(lastmodifieddate, 'YYYY-MM-DD\"T\"HH24:MI:SSTZH:TZM') as lastmodifieddatetime
        FROM customer
        order by lastmodifieddate ASC
        """
    primary_keys = ["id"]
    replication_key = "lastmodifieddatetime"


class InvoiceStream(suiteqlStream):
    name = "Invoice"
    path = "/query/v1/suiteql"
    metadata_path = "/record/v1/metadata-catalog/invoice"
    # Always sort the replication key and format the replication_key
    body_query = """
        select *
        ,TO_CHAR(lastmodifieddate, 'YYYY-MM-DD\"T\"HH24:MI:SSTZH:TZM') as lastmodifieddatetime
        FROM transaction where type = 'CustInvc'
        order by lastmodifieddate ASC
        """
    primary_keys = ["id"]
    replication_key = "lastmodifieddatetime"


class SubscriptionLineStream(suiteqlStream):
    name = "SubscriptionLine"
    path = "/query/v1/suiteql"
    metadata_path = "/record/v1/metadata-catalog/subscriptionline"
    # Always sort the replication key and format the replication_key
    body_query = """
        select *
        ,TO_CHAR(lastmodifieddate, 'YYYY-MM-DD\"T\"HH24:MI:SSTZH:TZM') as lastmodifieddatetime 
        FROM subscriptionline 
        order by lastmodifieddate ASC
        """
    primary_keys = ["id"]
    replication_key = "lastmodifieddatetime"


class SubscriptionPriceInterval(suiteqlStream):
    name = "SubscriptionPriceInterval"
    path = "/query/v1/suiteql"
    # Always sort the replication key and format the replication_key
    body_query = """
        select *
        FROM Subscriptionpriceinterval 
        """
    primary_keys = ["id"]
    schema = th.PropertiesList(
        th.Property("catalogtype", th.StringType),
        th.Property("chargetype", th.StringType),
        th.Property("enddate", th.StringType),
        th.Property("frequency", th.StringType),
        th.Property("id", th.StringType),
        th.Property("item", th.StringType),
        th.Property("linenumber", th.StringType),
        th.Property("priceplan", th.StringType),
        th.Property("prorateby", th.StringType),
        th.Property("proratebyoption", th.StringType),
        th.Property("quantity", th.StringType),
        th.Property("recurringamount", th.StringType),
        th.Property("repeatevery", th.StringType),
        th.Property("startdate", th.StringType),
        th.Property("startoffsetvalue", th.StringType),
        th.Property("status", th.StringType),
        th.Property("subscription", th.StringType),
    ).to_dict()
