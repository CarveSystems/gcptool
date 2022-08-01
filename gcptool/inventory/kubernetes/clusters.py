from typing import Any, List, Optional

from ..cache import Cache, with_cache
from . import api
from .types import Cluster


@with_cache("gke", "clusters")
def __list(project_id: str) -> List[Any]:
    # "Clusters in this project in all zones/locations"
    parent = f"projects/{project_id}/locations/-"

    request = api.clusters.list(parent=parent)
    response = request.execute()

    return response.get("clusters", [])


def __parse(raw: List[Any]) -> List[Cluster]:
    clusters: List[Cluster] = []

    for raw_cluster in raw:
        cluster = Cluster(**raw_cluster)
        clusters.append(cluster)

    return clusters


def list(project_id: str, cache: Cache) -> List[Cluster]:
    clusters = __list(cache, project_id)
    return __parse(clusters)
