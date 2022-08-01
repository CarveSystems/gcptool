import logging
from typing import Any, List, Optional

import gcptool.inventory.cloudfunctions as cloudfunctions
from gcptool.scanner.context import Context
from gcptool.scanner.finding import Finding, Severity
from gcptool.scanner.scan import Scan, ScanMetadata, scan


@scan
class CloudFunctionInventory(Scan):
    @staticmethod
    def meta():
        return ScanMetadata(
            "cloudfunctions",
            "triggerable",
            "Inventory of cloud functions",
            Severity.INFO,
            ["roles/iam.securityReviewer"],
        )

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
            logging.debug(instances)
            return self.finding(instances=instances)

        return None
