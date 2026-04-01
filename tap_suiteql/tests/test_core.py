"""Tests standard tap features using the built-in SDK tests library."""

from os import environ as env

from singer_sdk.testing import get_tap_test_class

from tap_suiteql.tap import Tapsuiteql

import pytest

# ...

if not env.get("TAP_SUITEQL_START_DATE"):
    pytest.skip("Missing TAP_SUITEQL_START_DATE, skipping tests", allow_module_level=True)

SAMPLE_CONFIG = {
    "start_date": env.get("TAP_SUITEQL_START_DATE"),
    "consumer_secret": env.get("TAP_SUITEQL_CONSUMER_SECRET"),
    "consumer_key": env.get("TAP_SUITEQL_CONSUMER_KEY"),
    "token_id": env.get("TAP_SUITEQL_TOKEN_ID"),
    "token_secret": env.get("TAP_SUITEQL_TOKEN_SECRET"),
    "account_id": env.get("TAP_SUITEQL_ACCOUNT_ID"),
    "base_url": env.get("TAP_SUITEQL_BASE_URL"),
}


# Run standard built-in tap tests from the SDK:
TestTapSuiteql = get_tap_test_class(
    tap_class=Tapsuiteql,
    config=SAMPLE_CONFIG
)


# TODO: Create additional tests as appropriate for your tap.
