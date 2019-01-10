
"""
Blizzard API CLI - Utilities for managing test resources.

Vaughn Kottler 01/07/19
"""

# built-in
import os

# internal
from blizzard_api.credentials import get_seconds

def get_item(name):
    """
    Retrieve a test resource by filename.

    :param name: String filename of the requested resource
    :returns: Absolute path to the requested resource
    """

    current_path = os.path.realpath(__file__)
    current_path = os.path.dirname(current_path)
    current_path = os.path.join(current_path, "data" + os.sep)
    return os.path.join(os.path.dirname(current_path), name)

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
