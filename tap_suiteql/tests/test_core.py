"""Tests standard tap features using the built-in SDK tests library."""

from os import environ as env

from singer_sdk.testing import get_standard_tap_tests

from tap_suiteql.tap import Tapsuiteql

SAMPLE_CONFIG = {
    "consumer_secret": env["CONSUMER_SECRET"],
    "consumer_key": env["CONSUMER_KEY"],
    "token_id": env["TOKEN_ID"],
    "token_secret": env["TOKEN_SECRET"],
    "account_id": env["ACCOUNT_ID"],
    "base_url": env["BASE_URL"],
}


# Run standard built-in tap tests from the SDK:
def test_standard_tap_tests():
    """Run standard tap tests from the SDK."""
    tests = get_standard_tap_tests(Tapsuiteql, config=SAMPLE_CONFIG)
    for test in tests:
        test()


# TODO: Create additional tests as appropriate for your tap.
