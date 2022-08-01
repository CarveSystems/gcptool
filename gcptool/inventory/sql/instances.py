from typing import Any, List

from gcptool.inventory.cache import Cache, with_cache

from . import api
from .types import DatabaseInstance


@with_cache("sql", "instances")
def __all(project_id: str) -> List[Any]:
    request = api.instances.list(project=project_id)

    instances = []

    while request is not None:
        response = request.execute()
        instances.extend(response.get("items", []))
        request = api.instances.list_next(previous_request=request, previous_response=response)

    return instances


def all(project: str, cache: Cache) -> List[DatabaseInstance]:
    data = __all(cache, project)

    instances: List[DatabaseInstance] = []

    for instance in data:
        instance = DatabaseInstance(**instance)
        instances.append(instance)

    return instances
