from typing import Optional

from gcptool.inventory.kubernetes import clusters

from ..context import Context
from ..finding import Finding, Severity
from ..scan import Scan, ScanMetadata, scan


@scan
class ListKubernetesClusters(Scan):
    @staticmethod
    def meta():
        return ScanMetadata(
            "gke",
            "cluster-list",
            "List of Kubernetes clusters",
            Severity.INFO,
            ["roles/iam.securityReviewer"],
        )

    def run(self, context: Context) -> Optional[Finding]:
        for project in context.projects:
            all_clusters = clusters.list(project.id, context.cache)
            print(f'All clusters: "{all_clusters}"')

        return None
