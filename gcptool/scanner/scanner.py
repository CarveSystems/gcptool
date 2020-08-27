from typing import Any, List, Set
import google.api_core.exceptions as gcperrors

import gcptool.scanner.scans
from gcptool.inventory import iam

from .context import Context
from .finding import Finding
from .scan import all_scans


class Scanner:
    def __init__(self):
        self.findings: List[Finding] = []

    def scan(self, context: Context) -> List[Finding]:
        print(f"Scanner: Beginning scan")

        all_findings: List[Finding] = []

        for scanner in all_scans:
            try:
                meta = scanner.meta()
                
                print(f"Running scanner {meta.name} for {meta.service}...")
                scan = scanner()
                finding = scan.run(context)
                if finding:
                    print(f"Complete. There is a potential finding.")
                    all_findings.extend(findings)
                else:
                    print(f"Complete.")

                print(f"Writing data to cache...")
                context.cache.save()
                continue
            
            except gcperrors.Forbidden as e:
                print(f"Insufficient permissions to complete this scan: {str(e)}")
                
            print(f"Aborted.")
                

        return all_findings

    def check_permissions(self, context: Context) -> List[str]:
        all_role_names: Set[str] = set()

        for project in context.projects:
            project_roles = iam.roles.grantable_roles(
                f"//cloudresourcemanager.googleapis.com/projects/{project.id}", context.cache
            )

            for role in project_roles:
                all_role_names.add(role.name)

        roles: List[Any] = []
        for name in all_role_names:
            definition = iam.roles.get(name, context.cache)
            roles.append(definition)

        print(roles)
        return []
