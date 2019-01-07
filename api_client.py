#!/usr/bin/env python3

"""
Script entry-point.
"""

# built-in
import sys

# internal
from blizzard_api.client import main

if __name__ == "__main__":
    sys.exit(main(sys.argv))
