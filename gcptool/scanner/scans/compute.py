from typing import List, Any

from gcptool.scanner.finding import Finding, Severity
from gcptool.scanner.scan import Scan, ScanMetadata, scan
from gcptool.scanner.context import Context

#from gcptool.inventory.storage import buckets

@scan
class Something(Scan):
    """
    This scan does something.
    """

    @staticmethod
    def meta():
        return ScanMetadata("compute", "name",
                            "",
                            Severity.HIGH,
                            ["roles/iam.securityReviewer"])

    def run(self, context: Context) -> Optional[Finding]:
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
