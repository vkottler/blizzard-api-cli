
"""
Blizzard API CLI - TestCache class.

Vaughn Kottler 01/09/19
"""

# built-in
import argparse
import os
import stat
import tempfile
import unittest

# internal
from blizzard_api.test.resources import get_item

# payload
from blizzard_api.cache import Cache, CacheError

#pylint:disable=too-few-public-methods
class DummyObject:
    """ For creating data that can't be serialized into JSON. """

class TestCache(unittest.TestCase):
    """ Testing the disk-based JSON cache. """

    def setUp(self):
        """ Create a cache object to be used by test cases. """

        self.cache = Cache(get_item("test_cache"))

    def tearDown(self):
        """ Restore test cache to its default state. """

        # make sure dummy bucket doesn't get deleted permanently
        if not self.cache.is_bucket("empty_bucket"):
            self.cache.add_bucket("empty_bucket")

    def test_is_bucket(self):
        """ Verify that bucket detection logic works. """

        self.assertTrue(self.cache.is_bucket("empty_bucket"))
        self.assertFalse(self.cache.is_bucket("bad_bucket"))
        self.cache.add_bucket("test_bucket")
        self.assertTrue(self.cache.is_bucket("test_bucket"))
        self.cache.remove_bucket("test_bucket")
        self.assertFalse(self.cache.is_bucket("test_bucket"))

    def test_remove_all_buckets(self):
        """ Verify that clearing the cache works. """

        self.cache.add_bucket("test_bucket1")
        self.cache.add_bucket("test_bucket2")
        self.cache.remove_all_buckets()
        self.assertFalse(self.cache.is_bucket("empty_bucket"))
        self.assertFalse(self.cache.is_bucket("test_bucket1"))
        self.assertFalse(self.cache.is_bucket("test_bucket2"))
        self.assertFalse(self.cache.get_bucket_names())

    def test_constructor_exceptions(self):
        """ Verify that constructor exceptions trigger when expected. """

        # check that illegal directories can't be created
        root_path = os.path.abspath(os.sep)
        self.assertRaises(argparse.ArgumentTypeError, Cache,
                          os.path.join(root_path, "illegal_dir"))

        # make a temporary directory not writeable
        temp_dir_name = tempfile.mkdtemp()
        permissions = os.stat(temp_dir_name).st_mode
        permissions = permissions & ~stat.S_IWUSR
        os.chmod(temp_dir_name, permissions)
        self.assertRaises(argparse.ArgumentTypeError, Cache, temp_dir_name)
        os.rmdir(temp_dir_name)

    def test_general_exceptions(self):
        """
        Verify that exceptions checking state of buckets trigger when expected.
        """

        self.assertRaises(CacheError, self.cache.add_bucket, "empty_bucket")
        self.assertRaises(CacheError, self.cache.get_bucket, "no_such_bucket")
        self.assertRaises(CacheError, self.cache.remove_bucket, "no_such_bucket")
        self.assertRaises(CacheError, self.cache.add_item, "no_such_bucket", {})

    def test_bucket_contents(self):
        """ Verify that manipulating bucket contents works. """

        self.cache.add_bucket("test_bucket")

        # test that data can be written and read back
        item1 = "test String"
        item2 = {"string": item1}
        self.cache.add_item("test_bucket", item1)
        self.cache.add_item("test_bucket", item2)
        cache_contents = self.cache.get_bucket("test_bucket")
        self.assertEqual(cache_contents[0], item1)
        self.assertEqual(cache_contents[1], item2)

        # test that non-serializable data can't be written
        bad_object = DummyObject()
        self.assertRaises(CacheError, self.cache.add_item, "test_bucket", bad_object)

        self.cache.remove_bucket("test_bucket")
