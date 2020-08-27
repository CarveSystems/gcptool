from dataclasses import dataclass
from typing import Any, List

from ..cache import Cache, with_cache
from . import api


@dataclass
class Role:
    name: str
    description: str


@with_cache("iam", "grantable_roles")
def __grantable_roles(resource: str):
    return (
        api.roles.queryGrantableRoles(body={"fullResourceName": resource})
        .execute()
        .get("roles", [])
    )


def grantable_roles(resource: str, cache: Cache):
    roles = __grantable_roles(cache, resource)

    parsed_roles: List[Role] = []

    for role in roles:
        parsed_roles.append(Role(role["name"], role["description"]))

    return parsed_roles


@with_cache("iam", "role")
def __get(name: str):
    return api.roles.get(name=name).execute()


def get(name: str, cache: Cache) -> Any:
    role_data = __get(cache, name)
    return role_data
