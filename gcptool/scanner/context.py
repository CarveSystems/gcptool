from dataclasses import dataclass
from typing import List

from gcptool.inventory.cache import Cache
from gcptool.inventory.resourcemanager.projects import Project


@dataclass
class Context:
    projects: List[Project]
    cache: Cache
