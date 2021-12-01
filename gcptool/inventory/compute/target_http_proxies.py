from typing import List

from . import api
from gcptool.inventory.cache import with_cache, Cache

from .types import TargetHttpProxy

@with_cache("compute", "target_http_proxies")
def __all(project_id: str):
    return api.target_http_proxies.list(project=project_id).execute().get("items", [])

def all(project_id: str, cache: Cache) -> List[TargetHttpProxy]:
    return [TargetHttpProxy(**proxy) for proxy in __all(cache, project_id)]
