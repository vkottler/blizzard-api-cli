
"""
Blizzard API CLI - MockJsonEndpoint class.

Vaughn Kottler 01/10/19
"""

# built-in
import os
import tempfile
import unittest

# internal
from blizzard_api.credentials import Credentials
from blizzard_api.test.mock_json_endpoint import MockJsonEndpoint
from blizzard_api.test.resources import get_item, get_fake_token

# payload
from blizzard_api.tokens import request_client_token
from blizzard_api.query import QueryEngine

class TestNetworking(unittest.TestCase):
    """ """

    def setUp(self):
        """ """

        # set up query engine
        creds = Credentials(get_item("good_cred_file.json"), None,
                            get_fake_token)
        self.query = QueryEngine(creds)

        # set up and start mock endpoint
        self.server = MockJsonEndpoint()
        self.server.start()
        self.address = "http://localhost:{0}".format(self.server.get_port())

    def tearDown(self):
        """ """

        # stop mocked endpoint
        self.server.stop()

    def test_client_token(self):
        """ """

        token_server = "{0}/oauth/token".format(self.address)
        # TODO

    def test_queries(self):
        """ """

        query_format_str = self.address + "/{0}/{1}"
        # TODO

    def test_icon_query(self):
        """ """

        icon_query_format_str = self.address + "icons/{0}/{1}"
        # TODO

        temp_dir_name = tempfile.mkdtemp()
        os.rmdir(temp_dir_name)
