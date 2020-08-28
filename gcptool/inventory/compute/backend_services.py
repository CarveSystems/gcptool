from typing import List

from . import api
from gcptool.inventory.cache import with_cache, Cache

@with_cache("compute", "backend_services")
def __all(project_id: str):
    return api.backend_services.list(project=project_id).execute().get("items", [])

def all(project_id: str, cache: Cache) -> List[str]:
    return [backend_service for backend_service in __all(cache, project_id)]
