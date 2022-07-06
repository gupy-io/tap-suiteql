"""Stream type classes for tap-suiteql."""

from tap_suiteql.client import suiteqlStream
from singer_sdk import typing as th


class SubscriptionStream(suiteqlStream):
    name = "Subscription"
    path = "/query/v1/suiteql"
    metadata_path = "/record/v1/metadata-catalog/subscription"
    primary_keys = ["id"]
    skip_attributes = ["links"]
    replication_key = "lastmodifieddate"


class CustomerStream(suiteqlStream):
    name = "Customer"
    path = "/query/v1/suiteql"
    metadata_path = "/record/v1/metadata-catalog/customer"
    primary_keys = ["id"]
    skip_attributes = ["links"]
    replication_key = "lastmodifieddate"


class InvoiceStream(suiteqlStream):
    name = "Invoice"
    path = "/query/v1/suiteql"
    metadata_path = "/record/v1/metadata-catalog/invoice"
    stream_type = (
        "CustInvc"  # When stream_type from transaction you should declare stream_type
    )
    primary_keys = ["id"]
    skip_attributes = ["links"]
    replication_key = "lastmodifieddate"


class SubscriptionLineStream(suiteqlStream):
    name = "SubscriptionLine"
    path = "/query/v1/suiteql"
    metadata_path = "/record/v1/metadata-catalog/subscriptionline"
    primary_keys = ["id"]
    skip_attributes = ["links"]
    replication_key = "lastmodifieddate"


class SubscriptionPriceIntervalStream(suiteqlStream):
    name = "SubscriptionPriceInterval"
    path = "/query/v1/suiteql"
    primary_keys = ["id"]
    schema = th.PropertiesList(
        th.Property("catalogtype", th.StringType),
        th.Property("chargetype", th.StringType),
        th.Property("enddate", th.DateTimeType),
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
        th.Property("startdate", th.DateTimeType),
        th.Property("startoffsetvalue", th.StringType),
        th.Property("status", th.StringType),
        th.Property("subscription", th.StringType),
    ).to_dict()


class SubscriptionPlanStream(suiteqlStream):
    name = "SubscriptionPlan"
    path = "/query/v1/suiteql"
    metadata_path = "/record/v1/metadata-catalog/subscriptionplan"
    primary_keys = ["id"]
    replication_key = "lastmodifieddate"
    skip_attributes = [
        "links",
        "incomeAccount",
    ]  # should match metadata endpoint attribute name


class ChangeOrderLineStream(suiteqlStream):
    name = "ChangeOrderLine"
    path = "/query/v1/suiteql"
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
        th.Property("subscriptionline", th.StringType),
    ).to_dict()


class CustomerPaymentStream(suiteqlStream):
    name = "CustomerPayment"
    path = "/query/v1/suiteql"

    stream_type = "CustPymt"
    primary_keys = ["id"]
    replication_key = "lastmodifieddate"
    schema = th.PropertiesList(
        th.Property("abbrevtype", th.StringType),
        th.Property("balsegstatus", th.StringType),
        th.Property("billingstatus", th.StringType),
        th.Property("closedate", th.DateTimeType),
        th.Property("createdby", th.StringType),
        th.Property("createddate", th.DateTimeType),
        th.Property("currency", th.StringType),
        th.Property("daysopen", th.StringType),
        th.Property("entity", th.StringType),
        th.Property("exchangerate", th.StringType),
        th.Property("foreignpaymentamountunused", th.StringType),
        th.Property("foreignpaymentamountused", th.StringType),
        th.Property("foreigntotal", th.StringType),
        th.Property("id", th.StringType),
        th.Property("includeinforecast", th.StringType),
        th.Property("isfinchrg", th.StringType),
        th.Property("isreversal", th.StringType),
        th.Property("lastmodifiedby", th.StringType),
        th.Property("lastmodifieddate", th.DateTimeType),
        th.Property("legacytax", th.StringType),
        th.Property("number", th.StringType),
        th.Property("onetime", th.StringType),
        th.Property("ordpicked", th.StringType),
        th.Property("paymenthold", th.StringType),
        th.Property("posting", th.StringType),
        th.Property("postingperiod", th.StringType),
        th.Property("printedpickingticket", th.StringType),
        th.Property("recordtype", th.StringType),
        th.Property("recurannually", th.StringType),
        th.Property("recurmonthly", th.StringType),
        th.Property("recurquarterly", th.StringType),
        th.Property("recurweekly", th.StringType),
        th.Property("status", th.StringType),
        th.Property("taxdetailsoverride", th.StringType),
        th.Property("taxpointdateoverride", th.StringType),
        th.Property("taxregoverride", th.StringType),
        th.Property("trandate", th.DateTimeType),
        th.Property("trandisplayname", th.StringType),
        th.Property("tranid", th.StringType),
        th.Property("transactionnumber", th.StringType),
        th.Property("type", th.StringType),
        th.Property("typebaseddocumentnumber", th.StringType),
        th.Property("userevenuearrangement", th.StringType),
        th.Property("visibletocustomer", th.StringType),
        th.Property("void", th.StringType),
        th.Property("voided", th.StringType),
    ).to_dict()


class CustomlistGpyCompanysizeStream(suiteqlStream):
    name = "customlist_gpy_companysize"
    path = "/query/v1/suiteql"
    metadata_path = "/record/v1/metadata-catalog/customlist_gpy_companysize"
    primary_keys = ["id"]
    skip_attributes = ["links"]


class CustomlistGpyReadjustmentindexStream(suiteqlStream):
    name = "customlist_gpy_readjustmentindex"
    path = "/query/v1/suiteql"
    metadata_path = "/record/v1/metadata-catalog/customlist_gpy_readjustmentindex"
    primary_keys = ["id"]
    skip_attributes = ["links"]
