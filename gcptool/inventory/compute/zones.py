from typing import List

from . import api
from gcptool.inventory.cache import with_cache, Cache

from .types import Zone

# TODO does it make sense to cache this by project id?
# - should drop project id as part of key if this data is the same across all projects

@with_cache("compute", "zones")
def __all(project_id: str):
    return api.zones.list(project=project_id).execute().get("items", [])

def all(project_id: str, cache: Cache) -> List[Zone]:
    return [Zone(**zone) for zone in __all(cache, project_id)]
