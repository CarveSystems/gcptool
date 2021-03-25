import dataclasses
import enum

from typing import List, Optional

@dataclasses.dataclass
class Expr:
    expression: str
    title: Optional[str]
    description: Optional[str]
    location: Optional[str]

@dataclasses.dataclass
class Binding:
    role: str
    members: List[str]
#    condition: Expr

@dataclasses.dataclass
class Policy:
    version: int
    bindings: List[Binding]
    audit_configs: dict
    etag: str
