from typing import Dict, List

from gcptool.inventory.cache import Cache, with_cache

from . import api
from .types import NetworkEndpointGroup


@with_cache("compute", "network_endpoint_groups")
def __all(project_id: str):
    network_endpoint_groups = []

    request = api.network_endpoint_groups.aggregatedList(project=project_id)

    while request is not None:
        response = request.execute()

        for region_data in response.get("items").values():
            for network_endpoint_group in region_data.get("networkEndpointGroups", []):
                network_endpoint_groups.append(network_endpoint_group)

        request = api.network_endpoint_groups.aggregatedList_next(
            previous_request=request, previous_response=response
        )

    return network_endpoint_groups


# a flat list of all network_endpoint_groups in project, for all zones
def all(project_id: str, cache: Cache) -> List[NetworkEndpointGroup]:
    return [
        NetworkEndpointGroup(**network_endpoint_group)
        for network_endpoint_group in __all(cache, project_id)
    ]
