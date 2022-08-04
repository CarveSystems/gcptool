from typing import Dict, List

from gcptool.inventory.cache import Cache, with_cache

from . import api
from .types import VpnGateway


@with_cache("compute", "vpn_gateways")
def __all(project_id: str):
    vpn_gateways = []

    request = api.vpn_gateways.aggregatedList(project=project_id)

    while request is not None:
        response = request.execute()

        for region_data in response.get("items").values():
            for vpn_gateway in region_data.get("vpnGateways", []):
                vpn_gateways.append(vpn_gateway)

        request = api.vpn_gateways.aggregatedList_next(
            previous_request=request, previous_response=response
        )

    return vpn_gateways


# a flat list of all vpn_gateways in project, for all regions
def all(project_id: str, cache: Cache) -> List[VpnGateway]:
    return [VpnGateway(**vpn_gateway) for vpn_gateway in __all(cache, project_id)]
