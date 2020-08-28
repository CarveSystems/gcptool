from typing import List

from . import api
from gcptool.inventory.cache import with_cache, Cache

@with_cache("compute", "vpn_gateways")
def __all(project_id: str):
    vpn_gateways = {}
    # TODO - we have no reference to the cache here, and so can't use
    ##for region in regions.all(project_id, cache):
    for region in api.regions.list(project=project_id).execute().get("items", []):
        region_vpn_gateways = api.vpn_gateways.list(project=project_id, region=region["name"]).execute().get("items", [])
        vpn_gateways[region["name"]] = region_vpn_gateways

    return vpn_gateways

# a flat list of all vpn_gateways in project, for all regions
def all(project_id: str, cache: Cache) -> List[str]:
    return [vpn_gateway for by_region in __all(cache, project_id).values() for vpn_gateway in by_region]

# nested lists of all vpn_gateways in project, by region
def by_region(project_id: str, cache: Cache) -> List[str]:
    vpn_gateways = {}
    for region,region_vpn_gateways in __all(cache, project_id).items():
        vpn_gateways[region] = [vpn_gateway for vpn_gateway in region_vpn_gateways]
    return vpn_gateways
