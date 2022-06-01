"""suiteql Authentication."""

from requests_oauthlib import OAuth1
from singer_sdk.authenticators import APIAuthenticatorBase, SingletonMeta
from singer_sdk.streams import Stream as RESTStreamBase


# The SingletonMeta metaclass makes your streams reuse the same authenticator instance.
# If this behaviour interferes with your use-case, you can remove the metaclass.
class suiteqlAuthenticator(APIAuthenticatorBase, metaclass=SingletonMeta):
    """Authenticator class for suiteql."""

    def __init__(
        self,
        stream: RESTStreamBase,
    ) -> None:
        super().__init__(stream=stream)

        self._consumer_secret = self.config["consumer_secret"]
        self._consumer_key = self.config["consumer_key"]
        self._token_id = self.config["token_id"]
        self._token_secret = self.config["token_secret"]
        self._account_id = self.config["account_id"]

    def oauth_object(self):
        return OAuth1(
            self._consumer_key,
            client_secret=self._consumer_secret,
            realm=self.config["account_id"],
            signature_method="HMAC-SHA256",
            resource_owner_key=self._token_id,
            resource_owner_secret=self._token_secret,
        )

    @classmethod
    def create_for_stream(
        cls,
        stream,
    ) -> "suiteqlAuthenticator":
        return cls(
            stream=stream,
        )
