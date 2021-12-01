from typing import Any, List

from ..cache import Cache, with_cache
from . import api
from .types import ServiceAccount, ServiceAccountKey

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
    return [ServiceAccount(**item) for item in __list(cache, f'projects/{project_name}')]

@with_cache("iam", "keys")
def __listKeys(name: str) -> List[Any]:
    name = f'projects/-/serviceAccounts/{name}'
    request = api.service_accounts.keys().list(name=name)
    response = request.execute()
    return response.get("keys", [])

def list_keys(sa: ServiceAccount, cache: Cache):
    return [ServiceAccountKey(**item) for item in __listKeys(cache, sa.unique_id)]