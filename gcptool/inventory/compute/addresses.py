from typing import List, Any

from . import api
from gcptool.inventory.cache import Cache

def addresses(project: str) -> List[object]:
    all_addresses = []

    r = regions(project)

    for region in r:
        region_addresses = address_api.list(project=project, region=region).execute()

        if "items" not in region_addresses:
            continue

        for address in region_addresses["items"]:
            all_addresses.append(address)

    return all_addresses
