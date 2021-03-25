from typing import List, Any

from googleapiclient.errors import HttpError

from . import api
from gcptool.inventory.cache import with_cache, Cache

@with_cache("cloudfunctions", "functions")
def __list(project_id):
    parent = f'projects/{project_id}/locations/-' 

    functions = []
    try:
        return api.functions.list(parent=parent).execute().get("functions", [])
    except HttpError:
        # TODO - We get a 403 here if the project hasn't enabled this API.
        # We should just detect if the API is enabled elsewhere and then just never call this function instead.
        return []

def list(project_id: str, cache: Cache) -> List[Any]:
    functions = __list(cache, project_id)
    return functions
