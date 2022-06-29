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


class SubscriptionPriceIntervalStream(suiteqlStream):
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


class SubscriptionPlanStream(suiteqlStream):
    name = "SubscriptionPlan"
    path = "/query/v1/suiteql"
    metadata_path = "/record/v1/metadata-catalog/subscriptionplan"
    # Always sort the replication key and format the replication_key
    body_query = """
        select *
        ,TO_CHAR(lastmodifieddate, 'YYYY-MM-DD\"T\"HH24:MI:SSTZH:TZM') as lastmodifieddatetime
        FROM subscriptionplan
        order by lastmodifieddate ASC
        """
    primary_keys = ["id"]
    replication_key = "lastmodifieddatetime"

class ChangeOrderLineStream(suiteqlStream):
    name = "ChangeOrderLine"
    path = "/query/v1/suiteql"
    body_query = """
        select *
        FROM changeorderline 
        """
    schema = th.PropertiesList(
        th.Property("discount", th.StringType),
        th.Property("item", th.StringType),
        th.Property("newdiscount", th.StringType),
        th.Property("newpriceplan", th.StringType),
        th.Property("newstatus", th.StringType),
        th.Property("priceplan", th.StringType),
        th.Property("sequence", th.StringType),
        th.Property("status", th.StringType),
        th.Property("subscriptionchangeorder", th.StringType),
        th.Property("subscriptionline", th.StringType)
    ).to_dict()

class CustomerPaymentStream(suiteqlStream):
    name = "CustomerPayment"
    path = "/query/v1/suiteql"
    body_query = """
        select *
        ,TO_CHAR(lastmodifieddate, 'YYYY-MM-DD\"T\"HH24:MI:SSTZH:TZM') as lastmodifieddatetime
        FROM transaction where type = 'CustPymt'
        """
    primary_keys = ["id"]
    replication_key = "lastmodifieddatetime"
    schema = th.PropertiesList(
        th.Property("abbrevtype",th.StringType),
        th.Property("balsegstatus",th.StringType),
        th.Property("billingstatus",th.StringType),
        th.Property("closedate",th.StringType),
        th.Property("createdby",th.StringType),
        th.Property("createddate",th.StringType),
        th.Property("currency",th.StringType),
        th.Property("daysopen",th.StringType),
        th.Property("entity",th.StringType),
        th.Property("exchangerate",th.StringType),
        th.Property("foreignpaymentamountunused",th.StringType),
        th.Property("foreignpaymentamountused",th.StringType),
        th.Property("foreigntotal",th.StringType),
        th.Property("id",th.StringType),
        th.Property("includeinforecast",th.StringType),
        th.Property("isfinchrg",th.StringType),
        th.Property("isreversal",th.StringType),
        th.Property("lastmodifiedby",th.StringType),
        th.Property("lastmodifieddate",th.StringType),
        th.Property("legacytax",th.StringType),
        th.Property("number",th.StringType),
        th.Property("onetime",th.StringType),
        th.Property("ordpicked",th.StringType),
        th.Property("paymenthold",th.StringType),
        th.Property("posting",th.StringType),
        th.Property("postingperiod",th.StringType),
        th.Property("printedpickingticket",th.StringType),
        th.Property("recordtype",th.StringType),
        th.Property("recurannually",th.StringType),
        th.Property("recurmonthly",th.StringType),
        th.Property("recurquarterly",th.StringType),
        th.Property("recurweekly",th.StringType),
        th.Property("status",th.StringType),
        th.Property("taxdetailsoverride",th.StringType),
        th.Property("taxpointdateoverride",th.StringType),
        th.Property("taxregoverride",th.StringType),
        th.Property("trandate",th.StringType),
        th.Property("trandisplayname",th.StringType),
        th.Property("tranid",th.StringType),
        th.Property("transactionnumber",th.StringType),
        th.Property("type",th.StringType),
        th.Property("typebaseddocumentnumber",th.StringType),
        th.Property("userevenuearrangement",th.StringType),
        th.Property("visibletocustomer",th.StringType),
        th.Property("void",th.StringType),
        th.Property("voided",th.StringType)
    ).to_dict()

