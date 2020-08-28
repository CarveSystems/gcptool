from dataclasses import dataclass
from typing import Any, List, Optional

from ..cache import Cache, with_cache
from . import api


@dataclass
class WorkloadIdentityConfig:
    workload_pool: str


@dataclass
class MasterAuth:
    username: Optional[str]
    password: Optional[str]


@dataclass
class Cluster:
    name: str
    description: Optional[str]
    logging_service: str
    workload_identity: Optional[WorkloadIdentityConfig]


@with_cache("gke", "clusters")
def __list(project_id: str) -> List[Any]:
    # "Clusters in this project in all zones/locations"
    parent = f"projects/{project_id}/locations/-"

    request = api.clusters.list(parent=parent)
    response = request.execute()

    return response.get("clusters", [])


def list(project_id: str, cache: Cache) -> List[Any]:
    return __list(cache, project_id)
