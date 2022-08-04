import logging
from cmath import polar
from email import policy
from typing import Optional

import gcptool.inventory.cloudfunctions as cloudfunctions
from gcptool.inventory.compute.types import Op
from gcptool.scanner.context import Context
from gcptool.scanner.finding import Finding, Severity
from gcptool.scanner.scan import Scan, ScanMetadata, scan


@scan
class CloudFunctionInventory(Scan):
    @staticmethod
    def meta() -> ScanMetadata:
        return ScanMetadata(
            "cloudfunctions",
            "inventory",
            "Inventory of Cloud Functions resources",
            Severity.INFO,
            ["roles/iam.securityReviewer"],
        )

    def run(self, context: Context) -> Optional[Finding]:

        for project in context.projects:
            functions = cloudfunctions.functions.list(project.id, context.cache)

            for function in functions:
                cloudfunctions.functions.get_iam_policy(function.name, context.cache)


@scan
class TriggerableCloudFunction(Scan):
    @staticmethod
    def meta():
        return ScanMetadata(
            "cloudfunctions",
            "triggerable",
            "Publicly-triggerable Cloud Function resources",
            Severity.INFO,
            ["roles/iam.securityReviewer"],
        )

    def run(self, context: Context):

        instances = {}

        for project in context.projects:

            triggerable = []

            for function in cloudfunctions.functions.list(project.id, context.cache):

                # There are three conditions required for a function to be triggerable:
                # 1. The function has an HTTPS trigger
                # 2. The function is public (i.e. not restricted to the project VPC)
                # 3. allUsers has been granted invocation access

                if not function.https_trigger:
                    continue

                if function.ingress_settings != function.ingress_settings.allow_all:
                    continue

                iam_policy = cloudfunctions.functions.get_iam_policy(function.name, context.cache)

                for binding in iam_policy.bindings:
                    if (
                        binding.role == "roles/cloudfunctions.invoker"
                        and "allUsers" in binding.members
                    ):
                        triggerable.append(function)
                        break

            if triggerable:
                instances[project.id] = triggerable

        if instances:
            logging.debug(instances)
            return self.finding(instances=instances)

        return None
