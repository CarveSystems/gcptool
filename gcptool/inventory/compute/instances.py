import dataclasses
from typing import Dict, List

from gcptool.inventory.cache import Cache, with_cache

from . import api
from .types import Instance


@with_cache("compute", "instances")
def __all(project_id: str):
    instances = []
    request = api.instances.aggregatedList(project=project_id)

    while request is not None:
        response = request.execute()

        for region_data in response.get("items").values():
            for instance in region_data.get("instances", []):
                instances.append(instance)

        request = api.instances.aggregatedList_next(
            previous_request=request, previous_response=response
        )

    return instances


# a flat list of all instances in project, for all zones
def all(project_id: str, cache: Cache) -> List[Instance]:
    return [Instance(**instance) for instance in __all(cache, project_id)]
