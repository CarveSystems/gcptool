from typing import List

from . import api
from gcptool.inventory.cache import with_cache, Cache

@with_cache("compute", "ssl_certs")
def __all(project_id: str):
    return api.ssl_certs.list(project=project_id).execute().get("items", [])

def all(project_id: str, cache: Cache) -> List[str]:
    return [ssl_cert for ssl_cert in __all(cache, project_id)]
