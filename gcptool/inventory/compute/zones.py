import functools
from typing import Set

from googleapiclient.discovery import build

from gcptool.creds import credentials

# pylint: disable=no-member
zone_api = build("compute", "v1", credentials=credentials).zones()


@functools.lru_cache(128, False)
def zones(project: str) -> Set[str]:
    all_zones = zone_api.list(project=project).execute()

    ret = set()
    for zone in all_zones["items"]:
        ret.add(zone["name"])

    return ret
