
"""
Blizzard API CLI - TestCredentials class.

Vaughn Kottler 01/09/19
"""

# built-in
import os
import tempfile
import unittest

# internal
from blizzard_api.cache import Cache
from blizzard_api.test.resources import get_item

# payload
from blizzard_api.credentials import Credentials, get_seconds

def get_fake_token(_id, _secret):
    """
    A function to use in place of the server-querying token function that
    requires usable credentials.
    """

    token_dict = {}
    token_dict["token_type"] = "bearer"
    token_dict["access_token"] = "AAAABBBBCCCCDDDDEEEEFFFFGGGGHHHHII"
    token_dict["expires_in"] = 86399
    token_dict["retrieved"] = get_seconds()
    return token_dict

class TestCredentials(unittest.TestCase):
    """ Testing token retrieval and storage. """

    def setUp(self):
        """ Set up Credentials object and a temporary cache. """

        self.temp_dir_name = tempfile.mkdtemp()
        self.cache = Cache(self.temp_dir_name)
        self.creds = Credentials(get_item("good_cred_file.json"), self.cache,
                                 get_fake_token)

    def tearDown(self):
        """ Clean up temporary cache. """

        self.cache.remove_all_buckets()
        os.rmdir(self.temp_dir_name)

    def test_get_token(self):
        """
        Test token retrieval and cache behavior, always fetch a new token
        when we expect it to not be cached to avoid flaky failures.
        """

        # check nominal case, writing to cache and then retrieving it
        expected_token = get_fake_token("", "")
        self.assertEqual(self.creds.get_token(), expected_token)
        self.assertTrue(self.creds.token_in_cache())
        self.assertEqual(self.creds.get_token(), expected_token)

        # trigger no cache logic
        self.creds.cache = None
        expected_token = get_fake_token("", "")
        self.assertEqual(self.creds.get_token(), expected_token)

        # trigger empty-cache logic
        self.creds.cache = self.cache
        self.cache.remove_all_buckets()
        self.cache.add_bucket("token")
        expected_token = get_fake_token("", "")
        self.assertEqual(self.creds.get_token(), expected_token)

        # test token expiring logic
        expected_token["retrieved"] = 0
        self.cache.remove_all_buckets()
        self.cache.add_bucket("token")
        self.cache.add_item("token", expected_token)
        expected_token = get_fake_token("", "")
        self.assertEqual(self.creds.get_token(), expected_token)
