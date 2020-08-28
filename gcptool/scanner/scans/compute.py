from typing import List, Any, Optional

from gcptool.scanner.finding import Finding, Severity
from gcptool.scanner.scan import Scan, ScanMetadata, scan
from gcptool.scanner.context import Context

import gcptool.inventory.compute as compute

@scan
class ComputeInventory(Scan):
    """
    This scan generates an inventory of Compute resources as an INFO finding.
    """

    @staticmethod
    def meta():
        return ScanMetadata("compute", "inventory",
                            "Inventory of Compute Resources",
                            Severity.INFO,
                            ["roles/iam.securityReviewer"])

    def run(self, context: Context) -> Optional[Finding]:
        for project in context.projects:
            zones = compute.zones.all(project.id, context.cache)
            print(zones)
            
        return None

# @scan
# class Something(Scan):
#     """
#     This scan does something.
#     """

#     @staticmethod
#     def meta():
#         return ScanMetadata("compute", "name",
#                             "",
#                             Severity.HIGH,
#                             ["roles/iam.securityReviewer"])

#     def run(self, context: Context) -> Optional[Finding]:
#         return None
