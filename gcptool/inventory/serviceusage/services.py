from typing import Any, List

from ..cache import Cache, with_cache
from . import api

from .types import GoogleApiServiceusageV1Service

@with_cache("serviceusage", "services")
def _all(project_id: str) -> List[Any]:
    """
    Get the list of services for a project.

    Args:
        project_id: The project ID.
        cache: The cache to use.

    Returns:
        A raw list of services.
    """

    services = []

    request = api.services.list(parent=f"projects/{project_id}")

    while request is not None:
        response = request.execute()
        services.extend(response.get("services", []))
        request = api.services.list_next(request, response)
    
    return services

def all(project_id: str, cache: Cache) -> List[GoogleApiServiceusageV1Service]:
    """
    Get the list of services for a project.

    Args:
        project_id: The project ID.
        cache: The cache to use.

    Returns:
        A list of services.
    """

    return [GoogleApiServiceusageV1Service(**service) for service in _all(cache, project_id)]


Mapping = {
    "gke": "container",
    "gcs": "storage-api",
    "sql": "sqladmin",
    "iam": "cloudresourcemanager",
}