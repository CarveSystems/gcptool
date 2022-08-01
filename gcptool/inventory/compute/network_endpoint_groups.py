from typing import Dict, List

from gcptool.inventory.cache import Cache, with_cache

from . import api
from .types import NetworkEndpointGroup


@with_cache("compute", "network_endpoint_groups")
def __all(project_id: str):
    network_endpoint_groups = {}
    # TODO - we have no reference to the cache here, and so can't use
    ##for zone in zones.all(project_id, cache):
    for zone in api.zones.list(project=project_id).execute().get("items", []):
        zone_network_endpoint_groups = (
            api.network_endpoint_groups.list(project=project_id, zone=zone["name"])
            .execute()
            .get("items", [])
        )
        network_endpoint_groups[zone["name"]] = zone_network_endpoint_groups

    return network_endpoint_groups


# a flat list of all network_endpoint_groups in project, for all zones
def all(project_id: str, cache: Cache) -> List[NetworkEndpointGroup]:
    return [
        NetworkEndpointGroup(**network_endpoint_group)
        for by_zone in __all(cache, project_id).values()
        for network_endpoint_group in by_zone
    ]


# nested lists of all network_endpoint_groups in project, by zone
def by_zone(project_id: str, cache: Cache) -> Dict[str, List[NetworkEndpointGroup]]:
    network_endpoint_groups = {}
    for zone, zone_network_endpoint_groups in __all(cache, project_id).items():
        network_endpoint_groups[zone] = [
            NetworkEndpointGroup(**network_endpoint_group)
            for network_endpoint_group in zone_network_endpoint_groups
        ]
    return network_endpoint_groups
