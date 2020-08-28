from typing import Any, Dict, List, Set
import google.api_core.exceptions as gcperrors

import gcptool.scanner.scans
from gcptool.inventory import iam
from gcptool.inventory.iam import permissions
from gcptool.inventory.resourcemanager import projects

from .context import Context
from .finding import Finding
from .scan import all_scans


class Scanner:
    def __init__(self, context: Context):
        self.findings: List[Finding] = []
        self.context = context

    def scan(self) -> List[Finding]:

        print("Scanner: Beginning scan")

        all_findings: List[Finding] = []

        for scanner in all_scans:
            try:
                meta = scanner.meta()
                
                print(f"Running scanner {meta.name} for {meta.service}...")
                scan = scanner()
                finding = scan.run(self.context)
                if finding:
                    print(f"Complete. There is a potential finding.")
                    all_findings.extend(findings)
                else:
                    print(f"Complete.")

                print(f"Writing data to cache...")
                self.context.cache.save()
                continue
            
            except gcperrors.Forbidden as e:
                print(f"Insufficient permissions to complete this scan: {str(e)}")
                
            print(f"Aborted.")

        return all_findings

    def test_permissions(self):

        all_roles = self.get_roles()

        for scan in all_scans:
            all_okay = True

            meta = scan.meta()

            print(f"Running permissions check for {meta.service}:{meta.name}...")

            declared_permissions = meta.permissions
            required_permissions: Set[str] = set()

            for permission in declared_permissions:

                # If we've declared a role in our list of permissions, replace it with all of its permissions.
                if permission in all_roles:
                    required_permissions |= all_roles[permission].included_permissions
                else:
                    required_permissions.add(permission)

            for project in self.context.projects:
                # Check to see which permissions we're able to test.
                testable_permissions = set(
                    permissions.query_testable_permissions(
                        self.context.cache,
                        f"//cloudresourcemanager.googleapis.com/projects/{project.id}",
                    )
                )

                # Check the permissions that we need, that we can test.
                testable_permissions &= required_permissions

                # If there are none... We're good to go for this project.
                if len(testable_permissions) == 0:
                    continue

                missing_permissions = projects.test_permissions(project.id, testable_permissions)

                if len(missing_permissions) != 0:
                    # If there are any missing permissions... we're not good to go :(
                    all_okay = False
                    print(f"Permissions check FAILED for project {project.id}")
                    print(f"Need the following permissions: {missing_permissions}")

            if not all_okay:
                print(
                    f"Cannot run scan {meta.service}:{meta.name} due to failed permissions check."
                )
            else:
                print(f"Permissions check succeeded for {meta.service}:{meta.name}!")

            print()

        self.context.cache.save()

    def get_roles(self) -> Dict[str, iam.roles.Role]:
        all_roles: Dict[str, iam.roles.Role] = {}

        for project in self.context.projects:
            project_roles = iam.roles.grantable_roles(
                f"//cloudresourcemanager.googleapis.com/projects/{project.id}", self.context.cache
            )

            for role in project_roles:
                all_roles[role.name] = role

        return all_roles
