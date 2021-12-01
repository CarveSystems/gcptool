from typing import List, Dict, Any

from . import api
from .types import ForwardingRule
from gcptool.inventory.cache import with_cache, Cache

@with_cache("compute", "forwarding_rules")
def __all(project_id: str) -> Dict[str, List[Any]]:
    return api.forwarding_rules.aggregatedList(project=project_id).execute().get("items", [])

def all(project_id: str, cache: Cache) -> List[ForwardingRule]:
    rules = []

    results = __all(cache, project_id)

    for zone in results.values():
        for rule in zone.get('forwardingRules', []):
            rules.append(ForwardingRule(**rule))

    return rules