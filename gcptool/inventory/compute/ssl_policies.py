from typing import List

from gcptool.inventory.cache import Cache, with_cache

from . import api
from .types import SslPolicy


@with_cache("compute", "ssl_policies")
def __all(project_id: str):
    return api.ssl_policies.list(project=project_id).execute().get("items", [])


def all(project_id: str, cache: Cache) -> List[SslPolicy]:
    return [SslPolicy(**ssl_cert) for ssl_cert in __all(cache, project_id)]
