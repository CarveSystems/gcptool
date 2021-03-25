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
                
                # If this exists, this is a Google-managed cluster.
                # (Cloud Composer)
                if cluster.resource_labels and 'goog-composer-environment' in cluster.resource_labels.keys():
                    continue

                # Even if we don't have master-authorized-networks,
                # this cluster is fine if it's private-only.
                if (
                    cluster.private_cluster_config
                    and cluster.endpoint == cluster.private_cluster_config.private_endpoint
                ):
                    continue

                if not cluster.master_authorized_networks_config.enabled:
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
        vulnerable_projects: Dict[str, Dict[str, List[clusters.Cluster]]] = {}
        service_accounts: Dict[str, str] = {}

        for project in context.projects:
            vulnerable_clusters: List[clusters.Cluster] = []
            high_risk_clusters: List[clusters.Cluster] = []

            project_clusters = clusters.list(project.id, context.cache)

            for cluster in project_clusters:

                # If this exists, this is a Google-managed cluster.
                # (Cloud Composer)
                # (Google, why are you doing this?)
                if cluster.resource_labels and 'goog-composer-environment' in cluster.resource_labels.keys():
                    continue

                # We're looking for clusters without Workload Identity
                # (which allows giving each workload a unique IAM role)

                high_privilege_account = None
                for node_pool in cluster.node_pools:
                    config = node_pool["config"]
                    # These correspond to "Allow Full Access to Google APIs"
                    if 'https://www.googleapis.com/auth/any-api' in config['oauthScopes']:
                        high_privilege_account = config["serviceAccount"]
                    elif 'https://www.googleapis.com/auth/cloud-platform' in config['oauthScopes']:
                        high_privilege_account = config["serviceAccount"]

                if not cluster.workload_identity_config:
                    vulnerable_clusters.append(cluster)

                    if high_privilege_account:
                        if high_privilege_account == 'default':
                            high_privilege_account = 'Compute Engine Default'
                        service_accounts[cluster.name] = high_privilege_account
                        high_risk_clusters.append(cluster)


            if len(vulnerable_clusters):
                vulnerable_projects[project.id] = {"all": vulnerable_clusters, "high_privilege": high_risk_clusters}

        if len(vulnerable_projects) != 0:
            return self.finding(instances=vulnerable_projects, service_accounts=service_accounts)

        return None

@scan
class MiscellaneousHardeningSettings(Scan):
    @staticmethod
    def meta():
        return ScanMetadata(
            "gke",
            "hardening",
            "Kubernetes Engine clusters do not use recommended hardening configuration",
            Severity.LOW,
            ["roles/iam.securityReviewer"]
        )

    def run(self, context: Context) -> Optional[Finding]:
        vuln_projects = {}

        for project in context.projects:

            basic_auth = []
            legacy_auth = []
            pod_security_policy = []
            network_policy = []

            for cluster in clusters.list(project.id, context.cache):

                # If this exists, this is a Google-managed cluster.
                # (Cloud Composer)
                if cluster.resource_labels and 'goog-composer-environment' in cluster.resource_labels.keys():
                    continue

                if cluster.legacy_abac.enabled:
                    legacy_auth.append(cluster.name)

                if cluster.master_auth.username and cluster.master_auth.password:
                    basic_auth.append(cluster.name)

                if not cluster.pod_security_policy_config.enabled:
                    pod_security_policy.append(cluster.name)

                if not cluster.network_policy or not cluster.network_policy.enabled:
                    print(cluster)
                    network_policy.append(cluster.name)

            if basic_auth or legacy_auth or pod_security_policy or network_policy:
                vuln_projects[project.id] = {"basic": basic_auth, "legacy": legacy_auth, "psp": pod_security_policy, "net": network_policy}

        if vuln_projects:
            return self.finding(instances=vuln_projects)
                
