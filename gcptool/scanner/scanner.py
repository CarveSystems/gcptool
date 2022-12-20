import logging
import sys
from typing import Any, Dict, List, Optional, Set

import google.api_core.exceptions as gcperrors

from gcptool.inventory import iam
from gcptool.inventory.iam import permissions
from gcptool.inventory.resourcemanager import projects
from gcptool.inventory.serviceusage import services

from .context import Context
from .finding import Finding
from .scan import all_scans


class Scanner:
    def __init__(self, context: Context):
        self.findings: List[Finding] = []
        self.context = context

    def check_scans(
        self, requested_services: Optional[Set[str]], requested_scans: Optional[Set[str]]
    ):

        enabled_scans = all_scans[::]

        if requested_services:
            found_services = set()

            for scan in all_scans:

                if scan.meta().service not in requested_services:
                    enabled_scans.remove(scan)
                    continue

                found_services.add(scan.meta().service)

            if len(found_services) != len(requested_services):
                missing_services = requested_services - found_services

                print(f"Scanner: The following unknown services were specified: {missing_services}")
                return False

        if requested_scans:
            found_scans = set()

            for scan in enabled_scans:

                if scan.meta().name not in requested_scans:
                    enabled_scans.remove(scan)
                    continue

                found_scans.add(scan.meta().name)

            if len(found_scans) != len(requested_scans):
                missing_scans = requested_scans - found_scans
                print(f"Scanner: The following unknown scans were specified: {missing_scans}")
                return False

        return True

    def scan(
        self, enabled_services: Optional[Set[str]], enabled_scans: Optional[Set[str]]
    ) -> List[Finding]:

        if not self.check_scans(enabled_services, enabled_scans):
            print(
                "A list of available scans and services can found by running  `gcptool list-scans`."
            )
            print("Aborting...")
            sys.exit(1)
            return []

        logging.info("Scanner: Beginning scan")

        all_findings: List[Finding] = []

        for scanner in all_scans:

            all_projects = self.context.projects[::]

            try:
                meta = scanner.meta()

                dirty_projects = []

                if enabled_services and meta.service not in enabled_services:
                    # Skip
                    continue

                if enabled_scans and meta.name not in enabled_scans:
                    # Skip
                    continue

                # skip checking IAM (which always works)
                if meta.service != "iam":
                    for project in self.context.projects:

                        try:
                            project_services = services.all_enabled(
                                project.number, self.context.cache
                            )
                        except Exception as e:
                            # we seem to get rate-limited here ...
                            logging.warning(
                                f"failed to get list of services for {project.number}, assuming all enabled"
                            )
                            logging.warning(str(e))
                            continue

                        mapped_name = services.Mapping.get(meta.service, meta.service)

                        api_name = (
                            f"projects/{project.number}/services/{mapped_name}.googleapis.com"
                        )

                        for service in project_services:
                            if service.name == api_name and service.state == service.state.enabled:
                                break
                        else:
                            logging.debug(
                                f"Skipping project {project.name} because {mapped_name} API is not enabled"
                            )

                            dirty_projects.append(project)

                for project in dirty_projects:
                    self.context.projects.remove(project)

                print(f"Running scanner {meta.name} for {meta.service}...")
                scan = scanner()
                finding = scan.run(self.context)
                if finding:
                    print(f"Complete. There is a potential finding.")
                    all_findings.append(finding)
                else:
                    print(f"Complete.")

                print(f"Writing data to cache...")
                self.context.cache.save()
                continue

            except gcperrors.Forbidden as e:
                logging.warning(f"Insufficient permissions to complete this scan: {str(e)}")

            finally:
                # Restore the projects list
                self.context.projects = all_projects

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
                    required_permissions |= set(all_roles[permission].included_permissions)
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
                    logging.error(f"Permissions check FAILED for project {project.id}")
                    logging.error(f"Need the following permissions: {missing_permissions}")

            if not all_okay:
                logging.error(
                    f"Cannot run scan {meta.service}:{meta.name} due to failed permissions check."
                )
            else:
                print(f"Permissions check succeeded for {meta.service}:{meta.name}!")

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
