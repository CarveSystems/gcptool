from typing import List

from . import api
from gcptool.inventory.cache import with_cache, Cache

from .types import BackendBucket

@with_cache("compute", "backend_buckets")
def __all(project_id: str):
    return api.backend_buckets.list(project=project_id).execute().get("items", [])

def all(project_id: str, cache: Cache) -> List[BackendBucket]:
    return [BackendBucket(**backend_bucket) for backend_bucket in __all(cache, project_id)]
