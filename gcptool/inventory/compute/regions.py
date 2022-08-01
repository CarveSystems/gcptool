from typing import List

from gcptool.inventory.cache import Cache, with_cache

from . import api
from .types import Region


@with_cache("compute", "regions")
def __all(project_id: str):
    return api.regions.list(project=project_id).execute().get("items", [])


def all(project_id: str, cache: Cache) -> List[Region]:
    return [Region(**region) for region in __all(cache, project_id)]
