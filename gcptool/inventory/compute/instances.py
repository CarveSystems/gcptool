from typing import List

from . import api
from gcptool.inventory.cache import with_cache, Cache

@with_cache("compute", "instances")
def __all(project_id: str):
    instances = {}
    # TODO - we have no reference to the cache here, and so can't use
    ##for zone in zones.all(project_id, cache):
    for zone in api.zones.list(project=project_id).execute().get("items", []):
        zone_instances = api.instances.list(project=project_id, zone=zone["name"]).execute().get("items", [])
        instances[zone["name"]] = zone_instances

    return instances

# a flat list of all instances in project, for all zones
def all(project_id: str, cache: Cache) -> List[str]:
    return [instance for by_zone in __all(cache, project_id).values() for instance in by_zone]

# nested lists of all instances in project, by zone
def by_zone(project_id: str, cache: Cache) -> List[str]:
    instances = {}
    for zone,zone_instances in __all(cache, project_id).items():
        instances[zone] = [instance for instance in zone_instances]
    return instances
