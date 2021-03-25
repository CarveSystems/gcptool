import enum

from dataclasses import dataclass, fields
from typing import Any, List, Optional

from gcptool.util import parse_dataclass
from ..cache import Cache, with_cache
from . import api

@dataclass
class WorkloadIdentityConfig:
    workload_pool: str
    identity_namespace: str
    identity_provider: str


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
class PodSecurityPolicyConfig:
    enabled: bool

@dataclass
class LegacyABAC:
    enabled: bool

class NetworkPolicyProvider(enum.Enum):
    Unspecified = 'PROVIDER_UNSPECIFIED'
    Calico = 'CALICO'

@dataclass
class NetworkPolicy:
    provider: NetworkPolicyProvider
    enabled: bool

class ClusterStatus(enum.Enum):
    Unspecified = 'STATUS_UNSPECIFIED'
    Provisioning = 'PROVISIONING'
    Running = 'RUNNING'
    Reconciling = 'RECONCILING'
    Stopping = 'STOPPING'
    Error = 'ERROR'
    Degraded = 'DEGRADED'

class EncryptionState(enum.Enum):
    Unknown = 'UNKNOWN'
    Encrypted = 'ENCRYPTED'
    Decrypted = 'DECRYPTED'

@dataclass
class DatabaseEncryption:
    state: EncryptionState
    key_name: str

## ADDONS

@dataclass
class FeatureDisabledToggle:
    disabled: bool

@dataclass
class FeatureEnabledToggle:
    enabled: bool

class IstioAuthMode(enum.Enum):
    NoAuth = 'AUTH_NONE'
    MutualTLS = 'AUTH_MUTUAL_TLS'

@dataclass
class IstioConfig:
    disabled: bool
    auth: IstioAuthMode

class LoadBalancerType(enum.Enum):
    Unspecified = 'LOAD_BALANCER_TYPE_UNSPECIFIED'
    External = 'LOAD_BALANCER_TYPE_EXTERNAL'
    Internal = 'LOAD_BALANCER_TYPE_INTERNAL'

@dataclass
class CloudRunConfig:
    disabled: bool
    load_balancer_type: LoadBalancerType

@dataclass
class AddonsConfig:
    http_load_balancing: FeatureDisabledToggle
    horizontal_pod_autoscaling: FeatureDisabledToggle
    kubernetes_dashboard: FeatureDisabledToggle
    network_policy_config: FeatureDisabledToggle
    istio_config: IstioConfig
    cloud_run_config: CloudRunConfig
    dns_cache_config: FeatureEnabledToggle
    config_connector_config: FeatureEnabledToggle
    gce_persistent_disk_csi_driver_config: FeatureEnabledToggle
    kalm_config: FeatureEnabledToggle
    

@dataclass
class Cluster:
    name: str
    description: str
    initial_node_count: int
    # TODO - this guy is a monster
    node_config: dict
    master_auth: MasterAuth
    logging_service: str
    monitoring_service: str
    network: str
    cluster_ipv4_cidr: str
    addons_config: AddonsConfig
    subnetwork: str
    # this needs to be dataclass'd eventually
    node_pools: List[dict]
    locations: List[str]
    enable_kubernetes_alpha: bool
    resource_labels: dict
    label_fingerprint: str
    legacy_abac: LegacyABAC
    network_policy: NetworkPolicy
    # as do these two
    ip_allocation_policy: dict
    maintenance_policy: dict
    # binary_authorization
    # autoscaling
    # and this one...
    network_config: dict
    private_cluster: bool
    master_ipv4_cidr_block: str
    # default_max_pods_constraint
    # resource_usage_export_config
    # authenticator_groups_config
    # vertical_pod_autoscaling
    # here, too
    shielded_nodes: dict
    release_channel: dict
    workload_identity_config: Optional[WorkloadIdentityConfig]
    cluster_telemetry: dict
    # tpu_config
    # notification_config
    # confidential_nodes
    self_link: str
    zone: str
    endpoint: str
    initial_cluster_version: str
    current_master_version: str
    current_node_version: str
    create_time: str
    status: ClusterStatus
    status_message: str
    node_ipv4_cidr_size: int
    services_ipv4_cidr: str
    instance_group_urls: List[str]
    current_node_count: int
    expire_time: str
    location: str
    enable_tpu: bool
    tpu_ipv4_cidr_block: str
    database_encryption: DatabaseEncryption
    # conditions
    # master
    # autopilot

    # these moved to the bottom because I've given them defaults
    master_authorized_networks_config: Optional[MasterAuthorizedNetworks] = MasterAuthorizedNetworks(False, [])
    pod_security_policy_config: Optional[PodSecurityPolicyConfig] = PodSecurityPolicyConfig(False)
    private_cluster_config: Optional[PrivateClusterConfig] = PrivateClusterConfig(False, '')


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
        cluster = parse_dataclass(raw_cluster, Cluster)
        clusters.append(cluster)

    return clusters


def list(project_id: str, cache: Cache) -> List[Cluster]:
    clusters = __list(cache, project_id)
    return __parse(clusters)
