from typing import List

from gcptool.inventory.cache import Cache, with_cache

from . import api
from .types import TargetSslProxy


@with_cache("compute", "target_ssl_proxies")
def __all(project_id: str):
    return api.target_ssl_proxies.list(project=project_id).execute().get("items", [])


def all(project_id: str, cache: Cache) -> List[TargetSslProxy]:
    return [TargetSslProxy(**proxy) for proxy in __all(cache, project_id)]
