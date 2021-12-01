from typing import List

from . import api
from gcptool.inventory.cache import with_cache, Cache

from .types import SslPolicy

@with_cache("compute", "ssl_policies")
def __all(project_id: str):
    return api.ssl_policies.list(project=project_id).execute().get("items", [])

def all(project_id: str, cache: Cache) -> List[SslPolicy]:
    return [SslPolicy(**ssl_cert) for ssl_cert in __all(cache, project_id)]
