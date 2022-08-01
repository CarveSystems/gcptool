from typing import Any, List

from gcptool.inventory.cache import Cache, with_cache

from . import api
from .types import User


@with_cache("sql", "users")
def __all(instance_id: str) -> List[Any]:

    project_id, instance_id = instance_id.split("/")

    request = api.users.list(project=project_id, instance=instance_id)

    users = []

    while request is not None:
        response = request.execute()
        users.extend(response.get("items", []))
        request = api.users.list_next(previous_request=request, previous_response=response)

    return users


def all(project: str, instance: str, cache: Cache) -> List[User]:
    # TODO caching hack
    data = __all(cache, f"{project}/{instance}")

    users: List[User] = []

    for instance in data:
        instance = User(**instance)
        users.append(instance)

    return users
