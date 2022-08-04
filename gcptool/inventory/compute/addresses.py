from typing import Dict, List

from gcptool.inventory.cache import Cache, parse_model_cache, with_cache

from . import api
from .types import Address


@with_cache("compute", "addresses")
def __all(project_id: str):
    addresses = []
    request = api.addresses.aggregatedList(project=project_id)
    while request is not None:
        response = request.execute()

        for region_data in response.get("items").values():
            for address in region_data.get("addresses", []):
                addresses.append(address)

        request = api.addresses.aggregatedList_next(
            previous_request=request, previous_response=response
        )

    return addresses


# a flat list of all addresses in project, for all regions
def all(project_id: str, cache: Cache) -> List[Address]:
    return [Address(**address) for address in __all(cache, project_id)]
