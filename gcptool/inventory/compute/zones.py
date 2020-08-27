from typing import Set

from . import api
from gcptool.inventory.cache import Cache

def zones(project: str) -> Set[str]:
    all_zones = zone_api.list(project=project).execute()

    ret = set()
    for zone in all_zones["items"]:
        ret.add(zone["name"])

    return ret
