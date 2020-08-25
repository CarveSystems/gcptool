from abc import ABCMeta, abstractmethod
from typing import Dict, List, TypeVar, Callable, Generic, Any, Type
from collections import defaultdict

from dataclasses import dataclass

from .finding import Finding


@dataclass
class ScanMetadata:
    # What service does this scan belong to?
    service: str
    # What is the name of this scan?
    name: str

    # A list of IAM permissions required to perform this scan.
    permissions: List[str]


class Scan(metaclass=ABCMeta):
    """
    The base class representing a scan to be performed.
    """

    @staticmethod
    @abstractmethod
    def meta() -> ScanMetadata:
        raise NotImplementedError("Scans must implement this method")

    @abstractmethod
    def run(self, project) -> List[Finding]:
        raise NotImplementedError("Scans must implement this method")


ScanType = Type[Scan]

all_scans: List[ScanType] = []
scans_by_service: Dict[str, List[ScanType]] = defaultdict(lambda: list())
scans_by_name: Dict[str, ScanType] = {}


def scan(s: ScanType) -> ScanType:
    meta = s.meta()

    # Add this scan to the list of all the scans we're able to do.

    all_scans.append(s)
    scans_by_service[meta.service].append(s)
    scans_by_name[meta.name] = s

    return s
