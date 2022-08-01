import enum
from dataclasses import dataclass, field
from typing import Any, Dict


class Severity(enum.IntEnum):
    INFO = 0
    LOW = 1
    MEDIUM = 2
    HIGH = 3
    CRITICAL = 4


@dataclass(init=False)
class Finding:
    template: str
    title: str
    severity: Severity
    vars: Dict[str, Any] = field(default_factory=dict)

    def __init__(self, template: str, title: str, severity: Severity, **kwargs):
        self.template = template
        self.title = title
        self.severity = severity
        self.vars = kwargs
