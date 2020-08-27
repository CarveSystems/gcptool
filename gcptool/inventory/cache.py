from typing import Dict, Any, Optional
from pathlib import Path

import json


class Cache:
    """
    Simple class for storing raw GCP API responses to disk.
    """

    VERSION = 1

    def __init__(self, filename: Path):
        self.filename = filename

        if self.filename.exists():
            with self.filename.open("r") as f:
                self.data: Dict[str, Dict[str, Dict[str, Any]]] = json.load(f)

            # We store a meta
            if self.get("meta", "gcptool", "version") != self.VERSION:
                raise RuntimeError("Cache file version does not match tool version!")
        else:
            # The file doesn't exist. Just set it up with defaults for now.
            self.data = {}
            self.store("meta", "gcptool", "version", self.VERSION)

    def save(self):
        """
        Write the cache to disk.
        """

        with self.filename.open("w") as f:
            json.dump(self.data, f, indent=2)

    def get(self, service: str, resource: str, project: str) -> Optional[Any]:
        service_data = self.data.get(service)

        if not service_data:
            return None

        resource_data = service_data.get(resource)

        if not resource_data:
            return None

        return resource_data.get(project)

    def store(self, service: str, resource: str, project: str, data: Any):
        service_data = self.data.get(service)

        if not service_data:
            service_data = {}
            self.data[service] = service_data

        resource_data = service_data.get(resource)
        if not resource_data:
            resource_data = {}
            service_data[resource] = resource_data

        resource_data[project] = data
