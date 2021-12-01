from typing import List, Any

from . import api
from .types import Firewall
from gcptool.inventory.cache import with_cache, Cache

@with_cache("compute", "firewalls")
def __all(project_id: str) -> List[Any]:
    return api.firewalls.list(project=project_id).execute().get("items", [])

def all(project_id: str, cache: Cache) -> List[Firewall]:
    return [Firewall(**firewall) for firewall in __all(cache, project_id)]
