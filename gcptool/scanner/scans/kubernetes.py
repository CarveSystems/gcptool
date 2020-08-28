from typing import Dict, List, Optional

from gcptool.inventory.kubernetes import clusters, nodepools

from ..context import Context
from ..finding import Finding, Severity
from ..scan import Scan, ScanMetadata, scan


@scan
class PubliclyAccessibleClusters(Scan):
    @staticmethod
    def meta():
        return ScanMetadata(
            "gke",
            "public",
            "Kubernetes Engine masters were publicly accessible",
            Severity.LOW,
            ["roles/iam.SecurityReviewer"],
        )

    def run(self, context: Context) -> Optional[Finding]:
        vulnerable_projects: Dict[str, List[clusters.Cluster]] = {}

        for project in context.projects:
            vulnerable_clusters: List[clusters.Cluster] = []

            project_clusters = clusters.list(project.id, context.cache)

            for cluster in project_clusters:

                # Even if we don't have master-authorized-networks,
                # this cluster is fine if it's private-only.
                if (
                    cluster.private_config
                    and cluster.endpoint == cluster.private_config.private_endpoint
                ):
                    continue

                if not cluster.master_authorized_networks.enabled:
                    vulnerable_clusters.append(cluster)

            if len(vulnerable_clusters) != 0:
                vulnerable_projects[project.id] = vulnerable_clusters

        if len(vulnerable_projects) != 0:
            return self.finding(instances=vulnerable_projects)

        return None


@scan
class EnforceWorkloadIdentity(Scan):
    @staticmethod
    def meta():
        return ScanMetadata(
            "gke",
            "metadata",
            "Kubernetes Engine clusters do not protect access to metadata",
            Severity.LOW,
            ["roles/iam.securityReviewer"],
        )

    def run(self, context: Context) -> Optional[Finding]:
        vulnerable_projects: Dict[str, List[clusters.Cluster]] = {}

        for project in context.projects:
            vulnerable_clusters: List[clusters.Cluster] = []

            project_clusters = clusters.list(project.id, context.cache)

            for cluster in project_clusters:

                # Just check to see if workload identity is enabled.

                # TODO - investigate metadata concealment.
                # This seems to have been removed as an option?

                # Also, it would be ideal to check the permissions the node is running with...
                # The lack of this allows for privilege escalation.
                if not cluster.workload_identity:
                    vulnerable_clusters.append(cluster)

            if len(vulnerable_clusters):
                vulnerable_projects[project.id] = vulnerable_clusters

        if len(vulnerable_projects) != 0:
            return self.finding(instances=vulnerable_projects)

        return None

