from typing import List, Dict

from . import api
from .types import Address
from gcptool.inventory.cache import with_cache, Cache

@with_cache("compute", "addresses")
def __all(project_id: str):
    addresses = {}
    # TODO - we have no reference to the cache here, and so can't use
    ##for region in regions.all(project_id, cache):
    for region in api.regions.list(project=project_id).execute().get("items", []):
        region_addresses = api.addresses.list(project=project_id, region=region["name"]).execute().get("items", [])
        addresses[region["name"]] = region_addresses

    return addresses

# a flat list of all addresses in project, for all regions
def all(project_id: str, cache: Cache) -> List[Address]:
    return [Address(**address) for by_region in __all(cache, project_id).values() for address in by_region]

# nested lists of all addresses in project, by region
def by_region(project_id: str, cache: Cache) -> Dict[str, List[Address]]:
    addresses = {}
    for region,region_addresses in __all(cache, project_id).items():
        addresses[region] = [Address(**address) for address in region_addresses]
    return addresses
