from typing import List

from gcptool.inventory.cache import Cache, parse_model_cache, with_cache

from . import api
from .types import CloudFunction, Policy


@with_cache("cloudfunctions", "functions")
def __list(project_id):
    parent = f"projects/{project_id}/locations/-"

    return api.functions.list(parent=parent).execute().get("functions", [])


@with_cache("cloudfunctions", "iam")
def __get_iam_policy(name):
    return api.functions.getIamPolicy(resource=name).execute()


def list(project_id: str, cache: Cache) -> List[CloudFunction]:
    functions = [
        parse_model_cache(function, CloudFunction) for function in __list(cache, project_id)
    ]
    return functions


def get_iam_policy(name: str, cache: Cache) -> Policy:
    data = __get_iam_policy(cache, name)
    return Policy(**data)
