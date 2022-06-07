"""Stream type classes for tap-suiteql."""

from tap_suiteql.client import suiteqlStream


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


class CustomerStream(suiteqlStream):
    name = "Customer"
    path = "/query/v1/suiteql"
    # Always sort the replication key and format the replication_key
    body_query = (
        "select * "
        ",TO_CHAR(lastmodifieddate, 'YYYY-MM-DD HH:MI:SS') as lastmodifieddatetime "
        "from customer "
        "order by TO_CHAR(lastmodifieddate, 'YYYY-MM-DD HH:MI:SS') ASC"
    )
    primary_keys = ["id"]
    replication_key = "lastmodifieddatetime"
