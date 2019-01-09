
"""
Blizzard API CLI - Credentials class.

Vaughn Kottler 01/07/19
"""

# built-in
import argparse
import json
import logging
import time

# internal
from .tokens import request_client_token

def get_seconds():
    """ Retrieve Epoch time in seconds. """

    millis = int(round(time.time() * 1000))
    return round(millis / 1000)

class Credentials:
    """ Credentials retrieval from JSON-formatted files. """

    log = logging.getLogger(__name__)

    def __init__(self, credentials_file, cache=None,
                 get_token_fn=request_client_token):
        """
        :param credentials_file: Path to a JSON file containing an
                                 object with 'id' and 'secret' fields
        :raises: argparse.ArgumentTypeError, for use with argparse
        """

        self.creds = None
        self.cache = cache
        self.get_token_fn = get_token_fn

        # verify file can be opened and decoded as JSON
        try:
            with open(credentials_file, "r") as creds_file:
                self.creds = json.load(creds_file)
        except (json.decoder.JSONDecodeError, FileNotFoundError) as exc:
            Credentials.log.error(exc)
            raise argparse.ArgumentTypeError(exc)

        # verify expected keys are present
        try:
            self.id = self.creds["id"]
            self.secret = self.creds["secret"]
        except KeyError as exc:
            Credentials.log.error("Missing key %s in credentials file.", exc)
            raise argparse.ArgumentTypeError(exc)

    def token_in_cache(self):
        """
        :returns: Boolean result of checking the cache for a token
        """

        if self.cache is None:
            return False
        if not self.cache.is_bucket("token"):
            return False
        if not self.cache.get_bucket("token"):
            return False
        return True

    def cache_token(self, token):
        """
        :param token: token object to cache
        """

        # make call idempotent
        if self.cache is None:
            return

        # always clear the previously used token
        if self.cache.is_bucket("token"):
            self.cache.remove_bucket("token")
        self.cache.add_bucket("token")
        self.cache.add_item("token", token)

    def get_new_token(self):
        """
        :returns: a new client_credentials access token
        """

        token = self.get_token_fn(self.id, self.secret)
        token["retrieved"] = get_seconds()
        self.cache_token(token)
        return token

    def get_token(self):
        """
        :returns: a valid client_credentials access token
        """

        # if there's no token in the cache, return a new one and attempt to
        # cache it
        if not self.token_in_cache():
            return self.get_new_token()

        # if there is one, make sure it's still valid and get a new one if
        # not
        token = self.cache.get_bucket("token")[0]
        current_seconds = get_seconds()
        if token["retrieved"] + token["expires_in"] < current_seconds:
            return self.get_new_token()
        return token
