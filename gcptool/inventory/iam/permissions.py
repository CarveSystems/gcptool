from typing import List

from ..cache import with_cache
from . import api


@with_cache("iam", "testable_permissions")
def query_testable_permissions(resource_name: str) -> List[str]:
    resp: List[str] = []

    body = {"fullResourceName": resource_name, "pageSize": 1000}

    while True:
        request = api.permissions.queryTestablePermissions(body=body)
        response = request.execute()

        for permission in response.get("permissions", []):
            resp.append(permission.get("name"))

        if "nextPageToken" not in response:
            return resp

        body["pageToken"] = response["nextPageToken"]
