import enum
from dataclasses import dataclass
from typing import Any, List, Optional

from gcptool.inventory.cache import Cache, with_cache

from . import api


class State(enum.Enum):
    PENDING_CREATE = "PENDING_CREATE"
    RUNNABLE = "RUNNABLE"


class SQLIPAddressType(enum.Enum):
    PRIMARY = "PRIMARY"
    PRIVATE = "PRIVATE"
    OUTGOING = "OUTGOING"
    # These should be fairly uncommon.
    MIGRATED_1ST_GEN = "MIGRATED_1ST_GEN"
    SQL_IP_ADDRESS_TYPE_UNSPECIFIED = "SQL_IP_ADDRESS_TYPE_UNSPECIFIED"


@dataclass
class SQLIPAddress:
    type: SQLIPAddressType
    ip_address: str
    time_to_retire: Optional[str]


@dataclass
class ACLEntry:
    value: str
    name: str


@dataclass
class IPConfiguration:
    ipv4_enabled: bool
    private_network: Optional[str]
    require_ssl: bool
    authorized_networks: List[ACLEntry]


@dataclass
class Instance:
    name: str
    state: State
    ip_configuration: IPConfiguration
    ip_addresses: List[SQLIPAddress]


def _parse(raw: Any) -> Instance:
    raw_ip_config = raw["settings"]["ipConfiguration"]
    raw_authorized_networks = raw_ip_config["authorizedNetworks"]

    authorized_networks: List[ACLEntry] = []
    for network in raw_authorized_networks:
        new_network = ACLEntry(network["value"], network["name"])
        authorized_networks.append(new_network)

    ip_configuration = IPConfiguration(
        raw_ip_config["ipv4Enabled"],
        raw_ip_config.get("privateNetwork"),
        raw_ip_config.get("requireSsl", False),
        authorized_networks,
    )

    state = State(raw["state"])

    ip_addresses: List[SQLIPAddress] = []
    for address in raw["ipAddresses"]:
        address = SQLIPAddress(
            SQLIPAddressType(address["type"]), address["ipAddress"], address.get("timeToRetire")
        )
        ip_addresses.append(address)

    instance = Instance(raw["name"], state, ip_configuration, ip_addresses)

    return instance


@with_cache("sql", "instances")
def __all(project_id: str):
    return api.instances.list(project=project_id).execute().get("items", [])


def all(project: str, cache: Cache) -> List[Instance]:
    data = __all(cache, project)

    instances: List[Instance] = []

    for instance in data:
        instance = _parse(instance)
        instances.append(instance)

    return instances
