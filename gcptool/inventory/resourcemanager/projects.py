import enum
from dataclasses import dataclass
from typing import Any, List, Set, NewType, Optional

from ..cache import Cache, with_cache
from . import api

from .types import Policy

# These classes are used to assist with deserialization of GCP project resources.
# TODO - unify this with the other dataclasses we're autogenerating.

class LifecycleState(enum.Enum):
    """
    Used by the GCP API to represent the
    """

    ACTIVE = "ACTIVE"
    DELETE_REQUESTED = "DELETE_REQUESTED"


class ParentType(enum.Enum):
    ORGANIZATION = "organization"
    FOLDER = "folder"


# TODO - this could probably be a union of organization/folder ID types.
ParentId = NewType("ParentId", int)


@dataclass
class Parent:
    """
    Represents a GCP project's parent in the organiation hierarchy.
    """

    type: ParentType
    id: ParentId


ProjectNumber = NewType("ProjectNumber", int)
ProjectId = NewType("ProjectId", str)


@dataclass
class Project:
    """
    Represents a GCP project.
    """

    number: ProjectNumber
    id: ProjectId
    name: str
    state: LifecycleState
    parent: Optional[Parent] = None


def all() -> List[Project]:
    """
    Retrieve a list of all GCP projects this account has access to.
    """
    response = api.projects.list().execute()

    return [_parse(project) for project in response.get("projects", [])]


@with_cache("resourcemanager", "project")
def __get(project_id: str) -> Any:
    return api.projects.get(projectId=project_id).execute()


def get(cache: Cache, project_id: str) -> Project:
    data = __get(cache, project_id)

    return _parse(data)


def _parse(raw: dict) -> Project:
    raw_parent = raw.get("parent")

    if raw_parent:
        parent: Optional[Parent] = Parent(raw_parent["type"], ParentId(raw_parent["id"]))
    else:
        parent = None

    return Project(
        ProjectNumber(raw["projectNumber"]),
        raw["projectId"],
        raw["name"],
        raw["lifecycleState"],
        parent,
    )

@with_cache("iam", "project")
def __get_iam_policy(project_id: str):
    return api.projects.getIamPolicy(resource=project_id, body={"options": {"requestedPolicyVersion": 3}}).execute()

def get_iam_policy(project_id: str, cache: Cache) -> Policy:
    raw_iam_policy = __get_iam_policy(cache, project_id)

    policy = Policy(**raw_iam_policy)

    return policy


def test_permissions(project_id: str, permissions: Set[str]) -> Set[str]:
    actual_permissions = set()
    permissions_to_check = list(permissions)

    while len(permissions_to_check) != 0:
        # GCP limits us to checking 100 permissions at a time
        body = {"permissions": list(permissions_to_check[:100])}
        permissions_to_check = permissions_to_check[100:]

        request = api.projects.testIamPermissions(resource=project_id, body=body)
        response = request.execute()

        actual_permissions |= set(response.get("permissions", []))

    missing_permissions = permissions - actual_permissions

    return missing_permissions

