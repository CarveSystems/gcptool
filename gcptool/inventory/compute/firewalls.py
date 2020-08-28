from typing import List

from . import api
from gcptool.inventory.cache import with_cache, Cache

@with_cache("compute", "firewalls")
def __all(project_id: str):
    return api.firewalls.list(project=project_id).execute().get("items", [])

def all(project_id: str, cache: Cache) -> List[str]:
    return [firewall for firewall in __all(cache, project_id)]
