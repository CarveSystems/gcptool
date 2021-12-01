from typing import List, Any, Optional

from gcptool.scanner.finding import Finding, Severity
from gcptool.scanner.scan import Scan, ScanMetadata, scan
from gcptool.scanner.context import Context

import gcptool.inventory.cloudfunctions as cloudfunctions

@scan
class CloudFunctionInventory(Scan):

    @staticmethod
    def meta():
        return ScanMetadata("cloudfunctions", "triggerable",
                            "Inventory of cloud functions",
                            Severity.INFO,
                            ["roles/iam.securityReviewer"])

    def run(self, context: Context):

        instances = {}

        for project in context.projects:

            triggerable = []

            for function in cloudfunctions.functions.list(project.id, context.cache):
                if function.https_trigger:
                    triggerable.append(function.name)

            if triggerable:
                instances[project.id] = triggerable
        

        if instances:
            print(instances)
            return self.finding(instances=instances)

        return None