import dataclasses
import enum
from typing import List

class FirewallDirection(enum.Enum):
    Egress = 'EGRESS'
    Ingress = 'INGRESS'
        
@dataclasses.dataclass
class FirewallAllowed:
    IPProtocol: str
    ports: List[str]


@dataclasses.dataclass
class FirewallDenied:
    ports: List[str]
    IPProtocol: str


class FirewallLogConfigMetadata(enum.Enum):
    Exclude_All_Metadata = 'EXCLUDE_ALL_METADATA'
    Include_All_Metadata = 'INCLUDE_ALL_METADATA'
        
@dataclasses.dataclass
class FirewallLogConfig:
    metadata: FirewallLogConfigMetadata
    enable: bool


@dataclasses.dataclass
class Firewall:
    direction: FirewallDirection
    description: str
    self_link: str
    creation_timestamp: str
    kind: str
    source_tags: List[str]
    destination_ranges: List[str]
    id: str
    priority: int
    target_tags: List[str]
    name: str
    network: str
    source_service_accounts: List[str]
    allowed: List[FirewallAllowed]
    denied: List[FirewallDenied]
    disabled: bool
    log_config: FirewallLogConfig
    target_service_accounts: List[str]
    source_ranges: List[str]


@dataclasses.dataclass
class MetadataItems:
    key: str
    value: str


@dataclasses.dataclass
class Metadata:
    fingerprint: str
    kind: str
    items: List[MetadataItems]


@dataclasses.dataclass
class ConfidentialInstanceConfig:
    enable_confidential_compute: bool


@dataclasses.dataclass
class Tags:
    fingerprint: str
    items: List[str]


@dataclasses.dataclass
class AdvancedMachineFeatures:
    threads_per_core: int
    enable_nested_virtualization: bool


class InstancePrivateIpv6GoogleAccess(enum.Enum):
    Enable_Bidirectional_Access_To_Google = 'ENABLE_BIDIRECTIONAL_ACCESS_TO_GOOGLE'
    Enable_Outbound_Vm_Access_To_Google = 'ENABLE_OUTBOUND_VM_ACCESS_TO_GOOGLE'
    Inherit_From_Subnetwork = 'INHERIT_FROM_SUBNETWORK'
        
class InstanceStatus(enum.Enum):
    Deprovisioning = 'DEPROVISIONING'
    Provisioning = 'PROVISIONING'
    Repairing = 'REPAIRING'
    Running = 'RUNNING'
    Staging = 'STAGING'
    Stopped = 'STOPPED'
    Stopping = 'STOPPING'
    Suspended = 'SUSPENDED'
    Suspending = 'SUSPENDING'
    Terminated = 'TERMINATED'
        
@dataclasses.dataclass
class ShieldedInstanceIntegrityPolicy:
    update_auto_learn_policy: bool


@dataclasses.dataclass
class AcceleratorConfig:
    accelerator_count: int
    accelerator_type: str


@dataclasses.dataclass
class CustomerEncryptionKey:
    sha256: str
    kms_key_name: str
    raw_key: str
    kms_key_service_account: str


class AttachedDiskInterface(enum.Enum):
    Nvme = 'NVME'
    Scsi = 'SCSI'
        
class GuestOsFeatureType(enum.Enum):
    Feature_Type_Unspecified = 'FEATURE_TYPE_UNSPECIFIED'
    Gvnic = 'GVNIC'
    Multi_Ip_Subnet = 'MULTI_IP_SUBNET'
    Secure_Boot = 'SECURE_BOOT'
    Sev_Capable = 'SEV_CAPABLE'
    Uefi_Compatible = 'UEFI_COMPATIBLE'
    Virtio_Scsi_Multiqueue = 'VIRTIO_SCSI_MULTIQUEUE'
    Windows = 'WINDOWS'
        
@dataclasses.dataclass
class GuestOsFeature:
    type: GuestOsFeatureType


class AttachedDiskType(enum.Enum):
    Persistent = 'PERSISTENT'
    Scratch = 'SCRATCH'
        
class AttachedDiskMode(enum.Enum):
    Read_Only = 'READ_ONLY'
    Read_Write = 'READ_WRITE'
        
class AttachedDiskInitializeParamsOnUpdateAction(enum.Enum):
    Recreate_Disk = 'RECREATE_DISK'
    Recreate_Disk_If_Source_Changed = 'RECREATE_DISK_IF_SOURCE_CHANGED'
    Use_Existing_Disk = 'USE_EXISTING_DISK'
        
AttachedDiskInitializeParamsLabels = dict
@dataclasses.dataclass
class AttachedDiskInitializeParams:
    on_update_action: AttachedDiskInitializeParamsOnUpdateAction
    source_snapshot: str
    resource_policies: List[str]
    disk_size_gb: str
    description: str
    source_image_encryption_key: CustomerEncryptionKey
    provisioned_iops: str
    labels: AttachedDiskInitializeParamsLabels
    source_snapshot_encryption_key: CustomerEncryptionKey
    disk_name: str
    disk_type: str
    source_image: str


class FileContentBufferFileType(enum.Enum):
    Bin = 'BIN'
    Undefined = 'UNDEFINED'
    X509 = 'X509'
        
@dataclasses.dataclass
class FileContentBuffer:
    content: str
    file_type: FileContentBufferFileType


@dataclasses.dataclass
class InitialStateConfig:
    pk: FileContentBuffer
    dbs: List[FileContentBuffer]
    keks: List[FileContentBuffer]
    dbxs: List[FileContentBuffer]


@dataclasses.dataclass
class AttachedDisk:
    index: int
    disk_encryption_key: CustomerEncryptionKey
    interface: AttachedDiskInterface
    device_name: str
    guest_os_features: List[GuestOsFeature]
    type: AttachedDiskType
    kind: str
    disk_size_gb: str
    auto_delete: bool
    licenses: List[str]
    boot: bool
    source: str
    mode: AttachedDiskMode
    initialize_params: AttachedDiskInitializeParams
    shielded_instance_initial_state: InitialStateConfig


@dataclasses.dataclass
class AliasIpRange:
    subnetwork_range_name: str
    ip_cidr_range: str


class AccessConfigNetworkTier(enum.Enum):
    Premium = 'PREMIUM'
    Standard = 'STANDARD'
        
class AccessConfigType(enum.Enum):
    Direct_Ipv6 = 'DIRECT_IPV6'
    One_To_One_Nat = 'ONE_TO_ONE_NAT'
        
@dataclasses.dataclass
class AccessConfig:
    external_ipv6_prefix_length: int
    network_tier: AccessConfigNetworkTier
    set_public_ptr: bool
    kind: str
    external_ipv6: str
    nat_i_p: str
    name: str
    public_ptr_domain_name: str
    type: AccessConfigType


class NetworkInterfaceStackType(enum.Enum):
    Ipv4_Ipv6 = 'IPV4_IPV6'
    Ipv4_Only = 'IPV4_ONLY'
    Unspecified_Stack_Type = 'UNSPECIFIED_STACK_TYPE'
        
class NetworkInterfaceNicType(enum.Enum):
    Gvnic = 'GVNIC'
    Unspecified_Nic_Type = 'UNSPECIFIED_NIC_TYPE'
    Virtio_Net = 'VIRTIO_NET'
        
class NetworkInterfaceIpv6AccessType(enum.Enum):
    External = 'EXTERNAL'
    Unspecified_Ipv6_Access_Type = 'UNSPECIFIED_IPV6_ACCESS_TYPE'
        
@dataclasses.dataclass
class NetworkInterface:
    network: str
    alias_ip_ranges: List[AliasIpRange]
    access_configs: List[AccessConfig]
    network_i_p: str
    subnetwork: str
    kind: str
    name: str
    ipv6_access_configs: List[AccessConfig]
    stack_type: NetworkInterfaceStackType
    nic_type: NetworkInterfaceNicType
    ipv6_access_type: NetworkInterfaceIpv6AccessType
    fingerprint: str
    ipv6_address: str


class ReservationAffinityConsumeReservationType(enum.Enum):
    Any_Reservation = 'ANY_RESERVATION'
    No_Reservation = 'NO_RESERVATION'
    Specific_Reservation = 'SPECIFIC_RESERVATION'
    Unspecified = 'UNSPECIFIED'
        
@dataclasses.dataclass
class ReservationAffinity:
    consume_reservation_type: ReservationAffinityConsumeReservationType
    values: List[str]
    key: str


@dataclasses.dataclass
class ShieldedInstanceConfig:
    enable_vtpm: bool
    enable_integrity_monitoring: bool
    enable_secure_boot: bool


@dataclasses.dataclass
class ServiceAccount:
    email: str
    scopes: List[str]


InstanceLabels = dict
class SchedulingOnHostMaintenance(enum.Enum):
    Migrate = 'MIGRATE'
    Terminate = 'TERMINATE'
        
class SchedulingNodeAffinityOperator(enum.Enum):
    In = 'IN'
    Not_In = 'NOT_IN'
    Operator_Unspecified = 'OPERATOR_UNSPECIFIED'
        
@dataclasses.dataclass
class SchedulingNodeAffinity:
    values: List[str]
    key: str
    operator: SchedulingNodeAffinityOperator


@dataclasses.dataclass
class Scheduling:
    on_host_maintenance: SchedulingOnHostMaintenance
    node_affinities: List[SchedulingNodeAffinity]
    location_hint: str
    min_node_cpus: int
    automatic_restart: bool
    preemptible: bool


@dataclasses.dataclass
class DisplayDevice:
    enable_display: bool


@dataclasses.dataclass
class Instance:
    metadata: Metadata
    label_fingerprint: str
    resource_policies: List[str]
    confidential_instance_config: ConfidentialInstanceConfig
    tags: Tags
    last_stop_timestamp: str
    can_ip_forward: bool
    deletion_protection: bool
    cpu_platform: str
    advanced_machine_features: AdvancedMachineFeatures
    name: str
    private_ipv6_google_access: InstancePrivateIpv6GoogleAccess
    status: InstanceStatus
    shielded_instance_integrity_policy: ShieldedInstanceIntegrityPolicy
    last_suspended_timestamp: str
    guest_accelerators: List[AcceleratorConfig]
    zone: str
    last_start_timestamp: str
    disks: List[AttachedDisk]
    network_interfaces: List[NetworkInterface]
    reservation_affinity: ReservationAffinity
    status_message: str
    fingerprint: str
    start_restricted: bool
    kind: str
    creation_timestamp: str
    hostname: str
    satisfies_pzs: bool
    shielded_instance_config: ShieldedInstanceConfig
    self_link: str
    service_accounts: List[ServiceAccount]
    id: str
    labels: InstanceLabels
    min_cpu_platform: str
    scheduling: Scheduling
    display_device: DisplayDevice
    description: str
    machine_type: str


class AddressAddressType(enum.Enum):
    External = 'EXTERNAL'
    Internal = 'INTERNAL'
    Unspecified_Type = 'UNSPECIFIED_TYPE'
        
class AddressIpVersion(enum.Enum):
    Ipv4 = 'IPV4'
    Ipv6 = 'IPV6'
    Unspecified_Version = 'UNSPECIFIED_VERSION'
        
class AddressPurpose(enum.Enum):
    Dns_Resolver = 'DNS_RESOLVER'
    Gce_Endpoint = 'GCE_ENDPOINT'
    Ipsec_Interconnect = 'IPSEC_INTERCONNECT'
    Nat_Auto = 'NAT_AUTO'
    Private_Service_Connect = 'PRIVATE_SERVICE_CONNECT'
    Shared_Loadbalancer_Vip = 'SHARED_LOADBALANCER_VIP'
    Vpc_Peering = 'VPC_PEERING'
        
class AddressNetworkTier(enum.Enum):
    Premium = 'PREMIUM'
    Standard = 'STANDARD'
        
class AddressStatus(enum.Enum):
    In_Use = 'IN_USE'
    Reserved = 'RESERVED'
    Reserving = 'RESERVING'
        
@dataclasses.dataclass
class Address:
    creation_timestamp: str
    address_type: AddressAddressType
    address: str
    network: str
    ip_version: AddressIpVersion
    purpose: AddressPurpose
    id: str
    prefix_length: int
    description: str
    network_tier: AddressNetworkTier
    users: List[str]
    subnetwork: str
    kind: str
    self_link: str
    status: AddressStatus
    name: str
    region: str


