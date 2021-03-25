from dataclasses import dataclass
import enum
from typing import Any, List, Set, Optional

from gcptool.util import parse_dataclass

from ..cache import Cache, with_cache
from . import api

@dataclass
class ServiceAccount:
    name: str
    project_id: str
    unique_id: str
    email: str
    display_name: str
    etag: str
    description: str
    oauth2_client_id: str
    disabled: bool

class KeyType(enum.Enum):
    Unspecified = 'KEY_TYPE_UNSPECIFIED'
    UserManaged = 'USER_MANAGED'
    SystemManaged = 'SYSTEM_MANAGED'

@dataclass
class ServiceAccountKey:
    name: str
    private_key_type: str
    key_algorithm: str
    private_key_data: Optional[str]
    public_key_data: Optional[str]
    valid_after_time: str
    valid_before_time: str
    key_origin: str
    key_type: KeyType


@with_cache("iam", "service_accounts")
def __list(project_name: str) -> List[Any]:
    resp: List[Any] = []

    request = api.service_accounts.list(name=project_name)

    while request is not None:
        response = request.execute()

        for account in response.get("accounts", []):
            resp.append(account)

        request = api.service_accounts.list_next(previous_request=request, previous_response=response)

    return resp

def list(project_name: str, cache: Cache):
    return [parse_dataclass(item, ServiceAccount) for item in __list(cache, f'projects/{project_name}')]

@with_cache("iam", "keys")
def __listKeys(name: str) -> List[Any]:
    name = f'projects/-/serviceAccounts/{name}'
    request = api.service_accounts.keys().list(name=name)
    response = request.execute()
    return response.get("keys", [])

def list_keys(sa: ServiceAccount, cache: Cache):
    return [parse_dataclass(item, ServiceAccountKey) for item in __listKeys(cache, sa.unique_id)]