import datetime
from typing import Dict, List, Optional

from gcptool.inventory.resourcemanager import projects
from gcptool.inventory.pubsub import topics
from gcptool.inventory.iam import service_accounts

from ..context import Context
from ..finding import Finding, Severity
from ..scan import Scan, ScanMetadata, scan


@scan
class PrimitiveIAMRoles(Scan):
    @staticmethod
    def meta():
        return ScanMetadata(
            "iam",
            "primitive",
            "Primitive IAM roles in use",
            Severity.LOW,
            ["roles/iam.SecurityReviewer"],
        )

    def run(self, context: Context) -> Optional[Finding]:

        instances = {}

        for project in context.projects:
            iam_policy = projects.get_iam_policy(project.id, context.cache)

            viewers = set()
            editors = set()
            owners = set()

            for binding in iam_policy.bindings:

                if binding.role == 'roles/viewer':
                    viewers = viewers.union(binding.members)
                elif binding.role == 'roles/editor':
                    editors = editors.union(binding.members)
                elif binding.role == 'roles/owner':
                    owners = owners.union(binding.members)

            viewers = [o.split(':')[1] for o in sorted(viewers)]
            editors = [o.split(':')[1] for o in sorted(editors)]
            owners =  [o.split(':')[1] for o in sorted(owners)]


            if viewers or editors or owners:
                instances[project.id] = {"viewers": viewers, "editors": editors, "owners": owners}

        if instances:
            return self.finding(instances=instances)

@scan
class PublicRoleBindings(Scan):
    @staticmethod
    def meta():
        return ScanMetadata(
            "iam",
            "public",
            "AAAA",
            Severity.LOW,
            ["roles/iam.SecurityReviewer"],
        )

    def run(self, context: Context) -> Optional[Finding]:

        instances = {}

        for project in context.projects:
            iam_policy = projects.get_iam_policy(project.id, context.cache)

            all_users = set()
            all_authenticated_users = set()

            for binding in iam_policy.bindings:

                if 'allUsers' in binding.members:
                    all_users.add(binding.role)
                
                if 'allAuthenticatedUsers' in binding.members:
                    all_authenticated_users.add(binding.role)

            if all_users or all_authenticated_users:
                instances[project.id] = {"public": all_users, "authenticated": all_authenticated_users}

        if instances:
            return self.finding(instances=instances)


@scan
class PublicPubSub(Scan):
    @staticmethod
    def meta():
        return ScanMetadata(
            "iam",
            "public_pubsub",
            "PubSub topics were world-sendable",
            Severity.LOW,
            ["roles/iam.SecurityReviewer"],
        )

    def run(self, context: Context) -> Optional[Finding]:

        instances = {}

        for project in context.projects:
            all_users = set()
            all_authenticated_users = set()

            project_topics = topics.list(project.id, context.cache)


            for topic in project_topics:
                iam_policy = topics.get_iam_policy(topic.name, context.cache)

                if not iam_policy.bindings:
                    continue

                for binding in iam_policy.bindings:

                    if 'allUsers' in binding.members:
                        all_users.add((binding.role, topic.name))
                    
                    if 'allAuthenticatedUsers' in binding.members:
                        all_authenticated_users.add((binding.role, topic.name))

            if all_users or all_authenticated_users:
                instances[project.id] = {"public": all_users, "authenticated": all_authenticated_users}

        if instances:
            return self.finding(instances=instances)

@scan
class UnrotatedServiceAccountKeys(Scan):
    @staticmethod
    def meta():
        return ScanMetadata(
            "iam",
            "key_rotation",
            "Un-rotated service account keys",
            Severity.LOW,
            ["roles/iam.SecurityReviewer"],
        )

    def run(self, context: Context) -> Optional[Finding]:

        instances = {}

        long_ago = datetime.datetime.now() - datetime.timedelta(days=100)

        for project in context.projects:
            unrotated_users = set()

            for service_account in service_accounts.list(project.id, context.cache):
                for key in service_accounts.list_keys(service_account, context.cache):
                    
                    valid_after_time = datetime.datetime.fromisoformat(key.valid_after_time[:-1])

                    if long_ago >= valid_after_time:
                        unrotated_users.add(service_account.email)

            if unrotated_users:
                instances[project.id] = unrotated_users

        if instances:
            return self.finding(instances=instances)



