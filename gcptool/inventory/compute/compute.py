from typing import List

from googleapiclient.discovery import build

from gcptool.creds import credentials

from . import zones

compute = build("compute", "v1", credentials=credentials)

# pylint: disable=no-member
instance_api = compute.instances()


def instances(project: str) -> List[object]:
    project_instances: List[object] = []

    project_zones = zones.zones(project)
    for zone in project_zones:

        zone_instances = instance_api.list(project=project, zone=zone).execute()

        if "items" not in zone_instances:
            continue

        for instance in zone_instances["items"]:
            project_instances.append(instance)

    return project_instances
