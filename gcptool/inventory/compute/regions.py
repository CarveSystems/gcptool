from .compute import compute

import functools
from typing import List

# pylint: disable=no-member
regions_api = compute.regions()


@functools.lru_cache(128, False)
def regions(project: str) -> List[str]:
    all_regions: List[str] = []

    for region in regions_api.list(project=project).execute()["items"]:
        name = region["name"]
        all_regions.append(name)

    return all_regions
