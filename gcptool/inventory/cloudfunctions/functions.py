from typing import Any, List

from googleapiclient.errors import HttpError

from gcptool.inventory.cache import Cache, with_cache

from . import api
from .types import CloudFunction


@with_cache("cloudfunctions", "functions")
def __list(project_id):
    parent = f"projects/{project_id}/locations/-"

    return api.functions.list(parent=parent).execute().get("functions", [])


def list(project_id: str, cache: Cache) -> List[CloudFunction]:
    functions = [CloudFunction(**function) for function in __list(cache, project_id)]
    return functions
