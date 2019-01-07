
"""
Blizzard API CLI - Application entry-point.

Vaughn Kottler 01/07/19
"""

# built-in
import argparse
import logging

# internal
from .credentials import Credentials
from .cache import Cache

def main(argv):
    """
    :param argv: A list of String input arguments
    :returns: Integer return code for use with sys.exit
    """

    # initialize logging
    logging.basicConfig(level=logging.INFO)

    # initialize parser
    desc = "Interact with the battle.net API."
    parser = argparse.ArgumentParser(description=desc)

    # initialize arguments
    help_str = "Path to JSON credentials file (default: '%(default)s')"
    parser.add_argument("-a", "--auth", default="credentials.json",
                        help=help_str, type=Credentials)
    help_str = "Path to a cache directory to use (default: '%(default)s')"
    parser.add_argument("-c", "--cache", default="cache", help=help_str,
                        type=Cache)

    # parse arguments
    try:
        args = parser.parse_args(argv[1:])
    except SystemExit:
        return 1

    # execute requested task
    print(args)

    return 0
