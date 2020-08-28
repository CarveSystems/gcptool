from typing import List, Any, Optional

from gcptool.scanner.finding import Finding, Severity
from gcptool.scanner.scan import Scan, ScanMetadata, scan
from gcptool.scanner.context import Context

import gcptool.inventory.compute as compute

@scan
class ComputeInventory(Scan):
    """
    This scan generates an inventory of Compute resources as an INFO finding.
    """

    @staticmethod
    def meta():
        return ScanMetadata("compute", "inventory",
                            "Inventory of Compute Resources",
                            Severity.INFO,
                            ["roles/iam.securityReviewer"])

    def run(self, context: Context) -> Optional[Finding]:
        for project in context.projects:
            #ensure that all data for compute gets into the cache
            zones = compute.zones.all(project.id, context.cache)
            regions = compute.regions.all(project.id, context.cache)
            addresses = compute.addresses.all(project.id, context.cache)
            instances = compute.instances.all(project.id, context.cache)
            backend_buckets = compute.backend_buckets.all(project.id, context.cache)
            backend_services = compute.backend_services.all(project.id, context.cache)
            vpn_gateways = compute.vpn_gateways.all(project.id, context.cache)
            firewalls = compute.firewalls.all(project.id, context.cache)
            network_endpoint_groups = compute.network_endpoint_groups.all(project.id, context.cache)
            ssl_certs = compute.ssl_certs.all(project.id, context.cache)
            target_http_proxies = compute.target_http_proxies.all(project.id, context.cache)
            target_https_proxies = compute.target_https_proxies.all(project.id, context.cache)
            target_ssl_proxies = compute.target_ssl_proxies.all(project.id, context.cache)
            target_tcp_proxies = compute.target_tcp_proxies.all(project.id, context.cache)

        # TODO an actual finding, if we want one
        return None

# @scan
# class Something(Scan):
#     """
#     This scan does something.
#     """

#     @staticmethod
#     def meta():
#         return ScanMetadata("compute", "name",
#                             "",
#                             Severity.HIGH,
#                             ["roles/iam.securityReviewer"])

#     def run(self, context: Context) -> Optional[Finding]:
#         return None
