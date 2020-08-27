from typing import List

from . import api

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
