from typing import List, Any

from gcptool.scanner.finding import Finding, Severity
from gcptool.scanner.scan import Scan, ScanMetadata, scan

from gcptool.inventory.sql import instances


@scan
class TLSEnforcement(Scan):
    """
    Checks that all Cloud SQL instances that are available on the public internet require SSL.
    """

    @staticmethod
    def meta():
        return ScanMetadata("sql", "tls", ["cloudsql.instances.list"])

    def run(self, project: str) -> List[Finding]:
        p = instances.all(project)

        open_instances: List[instances.Instance] = []

        for instance in p:

            has_public_ip = False
            for address in instance.ip_addresses:
                if address.type == instances.SQLIPAddressType.PRIMARY:
                    has_public_ip = True

            # We need to check if this is actually available over the internet.
            # If there's an IP, but no authorized networks, then this instance isn't actually public.
            # (Except for throug the Cloud SQL proxy, which always uses SSL.)
            has_authorized_networks = len(instance.ip_configuration.authorized_networks) > 0

            requires_ssl = instance.ip_configuration.require_ssl

            if has_public_ip and has_authorized_networks and not requires_ssl:
                open_instances.append(instance)

        if len(open_instances):
            return [
                Finding(
                    "sql_tls.md",
                    "Cloud SQL instances do not require TLS",
                    Severity.LOW,
                    instances=open_instances,
                )
            ]

        return []
