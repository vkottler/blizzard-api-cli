
"""
Blizzard API CLI - Querying Blizzard API endpoints.

Vaughn Kottler 01/10/19

request_results = query.request("data/wow/playable-class/index", "static-us")
request_results = query.request("data/wow/playable-class/1", "static-us")
request_results = query.request("wow/item/18803")
print(request_results)
query.get_icon(56, "spell_frost_frostshock", ".")

print(request_results["_links"])
for result in request_results["classes"]:
    print(result)
"""

# built-in
from enum import Enum
import logging
import os

# third-party
import requests

QUERY_FORMAT_STR = "https://{0}.api.blizzard.com/{1}"
CN_QUERY_FORMAT_STR = "https://gateway.battlenet.com.{0}/{1}"
ICON_QUERY_FORMAT_STR = "http://media.blizzard.com/wow/icons/{0}/{1}"

class Region(Enum):
    """
    See "Regions" table at:
    https://develop.battle.net/documentation/guides/regionality-partitions-and-localization
    """

    US = "us"
    EU = "eu"
    KR = "kr"
    TW = "tw"
    CN = "cn"

class Locale(Enum):
    """
    See "Region Host List" table at:
    https://develop.battle.net/documentation/guides/regionality-partitions-and-localization
    """

    # US
    en_US = "en_US"
    es_MX = "es_MX"
    pt_BR = "pt_BR"

    # Europe
    en_GB = "en_GB"
    es_ES = "es_ES"
    fr_FR = "fr_FR"
    ru_RU = "ru_RU"
    de_DE = "de_DE"
    pt_PT = "pt_PT"
    it_IT = "it_IT"

    # Korea
    ko_KR = "ko_KR"

    # Taiwan
    zh_TW = "zh_TW"

    # China
    zh_CN = "zh_CN"

class Namespace(Enum):
    """
    See "World of Warcraft Namespaces" table at:
    https://develop.battle.net/documentation/guides/game-data-apis-wow-namespaces
    """

    Static = "static-{0}"
    Dynamic = "dynamic-{0}"
    Profile = "profile-{0}"

class IconSize(Enum):
    """
    Required parameter for retrieving in-game icons. See:
    https://us.battle.net/forums/en/bnet/topic/20755767469
    """

    SMALL = 18
    MEDIUM = 36
    LARGE = 56

class QueryEngine:
    """ Query builder and executor for battle.net APIs. """

    log = logging.getLogger(__name__)

    def __init__(self, credentials, region=Region.US,
                 locale=Locale.en_US):
        """
        :param credentials: Credentials object to perform valid queries with
        :param region: Region enum selection
        :param locale: Locale enum selection
        """

        self.credentials = credentials
        self.region = region
        self.locale = locale

    def request(self, path, namespace=None, query_format_str=QUERY_FORMAT_STR):
        """
        :param path: String path of the API endpoint to query
        :param namespace: Namespace enum selection, required for some queries
        :returns: JSON result as a dictionary
        """

        args = {"locale": self.locale,
                "access_token": self.credentials.get_token()["access_token"]}
        if namespace is not None:
            args["namespace"] = namespace.format(self.region)
        req = requests.get(query_format_str.format(self.region, path),
                           params=args)

        # request succeeded, return to user
        if req.status_code == requests.codes.ok:
            return req.json()

        # request failed, raise exception
        req.raise_for_status()
        return None

    @staticmethod
    def get_icon(name, dest_dir=".", size=IconSize.LARGE,
                 endpoint_format_str=ICON_QUERY_FORMAT_STR):
        """
        Retrieve an in-game icon by name.

        :param name: String name of the icon to retrieve
        :param dest_dir: String path to a directory to place the image file
        :param size: IconSize enum selection
        """

        # build the request uri
        file_name = "{0}.jpg".format(name)

        # perform and validate the request
        req = requests.get(endpoint_format_str.format(size, file_name),
                           stream=True)
        if req.status_code != requests.codes.ok:
            req.raise_for_status()

        # write the file contents
        with open(os.path.join(dest_dir, file_name), "wb") as img_fd:
            for chunk in req.iter_content(chunk_size=256):
                img_fd.write(chunk)
