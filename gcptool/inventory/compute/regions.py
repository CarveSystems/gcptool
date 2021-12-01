from typing import List

from . import api
from gcptool.inventory.cache import with_cache, Cache

from .types import Region

@with_cache("compute", "regions")
def __all(project_id: str):
    return api.regions.list(project=project_id).execute().get("items", [])

def all(project_id: str, cache: Cache) -> List[Region]:
    return [Region(**region) for region in __all(cache, project_id)]
