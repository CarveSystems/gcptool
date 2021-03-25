import dataclasses
import enum
from typing import List, Any

import netaddr

from gcptool.util import parse_dataclass

from . import api
from gcptool.inventory.cache import with_cache, Cache

class RuleDirection(enum.Enum):
    Ingress = "INGRESS"
    Egress = "EGRESS"

@dataclasses.dataclass
class FirewallRule:
    id: str
    creation_timestamp: str
    name: str
    description: str
    network: str
    priority: int
    source_ranges: List[str]
    destination_ranges: List[netaddr.IPNetwork]
    source_tags: set
    target_tags: set
    source_service_accounts: List[str]
    target_service_accounts: List[str]
    allowed: List[dict]
    denied: List[dict]
    direction: RuleDirection
    log_config: dict
    self_link: str
    kind: str
    disabled: bool = False

@with_cache("compute", "firewalls")
def __all(project_id: str) -> List[Any]:
    return api.firewalls.list(project=project_id).execute().get("items", [])

def all(project_id: str, cache: Cache) -> List[FirewallRule]:
    return [parse_dataclass(firewall, FirewallRule) for firewall in __all(cache, project_id)]
