from typing import List

from . import api
from gcptool.inventory.cache import with_cache, Cache

@with_cache("compute", "zones")
def __all(project_id: str):
    return api.zones.list(project=project_id).execute().get("items", [])

def all(project_id: str, cache: Cache) -> List[str]:
    return [zone["name"] for zone in __all(cache, project_id)]
