
"""
Blizzard API CLI - Cache class.

Vaughn Kottler 01/07/19
"""

# built-in
import argparse
import json
import logging
import os

class CacheError(Exception):
    """ Custom exception for use with the Cache class. """

class Cache:
    """ Disk-based cache implementation. """

    log = logging.getLogger(__name__)

    def __init__(self, cache_directory):
        """
        :param cache_directory: Path to an existing cache directory or a
                                location that one should be created
        :raises: argparse.ArgumentTypeError, for use with argparse
        """

        # ensure access to this directory (or viability of creation)
        if not os.path.isdir(cache_directory):
            try:
                os.makedirs(cache_directory)
            except OSError as exc:
                Cache.log.error(exc)
                raise argparse.ArgumentTypeError(exc)

        # check for read and write access
        if not os.access(cache_directory, os.O_RDWR):
            error_str = "Don't have read and write access to '{0}'.".format(cache_directory)
            Cache.log.error(error_str)
            raise argparse.ArgumentTypeError(error_str)

        self.directory = cache_directory

    def bucket_path(self, name):
        """
        :param name: String name of the bucket
        :returns: String path to the fully-qualified bucket file
        """

        return os.path.join(self.directory, "{0}.json".format(name))

    def add_bucket(self, name):
        """
        :param name: String name of the new bucket to add
        :raises: CacheError if the bucket is already present
        """

        # ensure bucket isn't already present
        if self.is_bucket(name):
            error_str = "Can't add bucket '{0}', it exists.".format(name)
            Cache.log.error(error_str)
            raise CacheError(error_str)

        # add empty list to new bucket file
        with open(self.bucket_path(name), "w") as bucket_file:
            bucket_file.write(json.dumps([]))

    def get_bucket(self, name):
        """
        :param name: String name of the bucket to retrieve
        :returns: deserialized content that the bucket contained
        :raises: CacheError if the bucket does not exist
        """

        # ensure bucket is present
        if not self.is_bucket(name):
            error_str = "Can't remove bucket '{0}', it doesn't exist.".format(name)
            Cache.log.error(error_str)
            raise CacheError(error_str)

        # read and return the deserialized contents
        content = None
        with open(self.bucket_path(name), "r") as bucket_file:
            content = json.load(bucket_file)
        return content

    def remove_bucket(self, name):
        """
        :param name: String name of the bucket to be removed
        :raises: CacheError if the bucket does not exist
        """

        # ensure bucket is present
        if not self.is_bucket(name):
            error_str = "Can't remove bucket '{0}', it doesn't exist.".format(name)
            Cache.log.error(error_str)
            raise CacheError(error_str)

        # remove file
        os.remove(self.bucket_path(name))

    def remove_all_buckets(self):
        """ Clear the cache of all existing data. """

        buckets = self.get_bucket_names()
        for bucket in buckets:
            self.remove_bucket(bucket)

    def add_item(self, bucket_name, item):
        """
        :param bucket_name: String name of bucket to add item to
        :param item: arbitrary object to be serialized into JSON and added
        :raises: CacheError if 'item' cannot be serialized into JSON
        """

        # ensure bucket is present
        if not self.is_bucket(bucket_name):
            error_str = "Can't add item to '{0}', it doesn't exist.".format(bucket_name)
            Cache.log.error(error_str)
            raise CacheError(error_str)

        # append the item to the existing bucket contents
        existing_contents = self.get_bucket(bucket_name)
        existing_contents.append(item)
        try:
            string_content = json.dumps(existing_contents, indent=4)
        except TypeError as exc:
            Cache.log.error(exc)
            raise CacheError(exc)

        # write contents back
        with open(self.bucket_path(bucket_name), "w") as bucket_file:
            bucket_file.write(string_content)

    def is_bucket(self, name):
        """
        :param name: String name of bucket to query
        :returns: Boolean status, true if the bucket exists
        """

        buckets = self.get_bucket_names()
        return name in buckets

    def get_bucket_names(self):
        """
        :returns: list of Strings of all existing buckets in this cache
        """

        return [file_name.strip(".json") for file_name in os.listdir(self.directory)]
