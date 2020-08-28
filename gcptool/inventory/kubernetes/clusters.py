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
class CIDRBlock:
    display_name: str
    cidr_block: str


@dataclass
class PrivateClusterConfig:
    # There are a bunch more here...
    # But these are the ones I want.
    enable_private_endpoint: bool
    private_endpoint: str


@dataclass
class MasterAuthorizedNetworks:
    enabled: bool
    cidr_blocks: List[CIDRBlock]


@dataclass
class Cluster:
    name: str
    location: str
    endpoint: str
    workload_identity: Optional[WorkloadIdentityConfig]
    private_config: Optional[PrivateClusterConfig]
    master_authorized_networks: MasterAuthorizedNetworks


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
        raw_workload_identity = raw_cluster.get("workloadIdentityConfig")

        if raw_workload_identity:
            workload_identity: Optional[WorkloadIdentityConfig] = WorkloadIdentityConfig(
                raw_workload_identity["workloadPool"]
            )
        else:
            workload_identity = None

        raw_private_config = raw_cluster.get("privateClusterConfig")

        if raw_private_config:
            private_config: Optional[PrivateClusterConfig] = PrivateClusterConfig(
                raw_private_config["enablePrivateEndpoint"], raw_private_config["privateEndpoint"]
            )
        else:
            private_config = None

        raw_man = raw_cluster["masterAuthorizedNetworksConfig"]
        man = MasterAuthorizedNetworks(raw_man.get("enabled", False), raw_man.get("cidrBlocks", []))

        cluster = Cluster(
            raw_cluster["name"],
            raw_cluster["location"],
            raw_cluster["endpoint"],
            workload_identity,
            private_config,
            man,
        )

        clusters.append(cluster)

    return clusters


def list(project_id: str, cache: Cache) -> List[Cluster]:
    clusters = __list(cache, project_id)
    return __parse(clusters)
