"""Tests standard tap features using the built-in SDK tests library."""

from os import environ as env

from singer_sdk.testing import get_tap_test_class

from tap_suiteql.tap import Tapsuiteql

SAMPLE_CONFIG = {
    "start_date": env.get("TAP_SUITEQL_START_DATE", "2021-01-01T00:00:00Z"),
    "consumer_secret": env.get("TAP_SUITEQL_CONSUMER_SECRET", "test"),
    "consumer_key": env.get("TAP_SUITEQL_CONSUMER_KEY", "test"),
    "token_id": env.get("TAP_SUITEQL_TOKEN_ID", "test"),
    "token_secret": env.get("TAP_SUITEQL_TOKEN_SECRET", "test"),
    "account_id": env.get("TAP_SUITEQL_ACCOUNT_ID", "test"),
    "base_url": env.get("TAP_SUITEQL_BASE_URL", "https://test.com"),
}


# Run standard built-in tap tests from the SDK:
TestTapSuiteql = get_tap_test_class(
    tap_class=Tapsuiteql,
    config=SAMPLE_CONFIG
)


# TODO: Create additional tests as appropriate for your tap.
