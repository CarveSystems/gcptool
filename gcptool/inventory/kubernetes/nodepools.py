from typing import Any, List

from ..cache import Cache, with_cache
from . import api


@with_cache("container", "nodepool")
def __list(parent: str) -> List[Any]:
    request = api.node_pools.list(parent=parent)
    response = request.execute()
    return response.get("nodePools", [])


def list(project_id: str, location: str, cluster_id: str, cache: Cache) -> List[Any]:
    parent = f"projects/{project_id}/locations/{location}/clusters/{cluster_id}"
    return __list(cache, parent)
