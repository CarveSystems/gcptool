from collections import defaultdict
from typing import List, Any, Optional

from netaddr import IPSet, IPAddress, iprange_to_globs

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
            print(f'Gathering inventory for {project.id}')

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

@scan
class IPAddressDump(Scan):

    @staticmethod
    def meta():
        return ScanMetadata("compute", "esm",
                            "Inventory of IP addresses",
                            Severity.INFO,
                            ["roles/iam.securityReviewer"])

    def run(self, context: Context) -> Optional[Finding]:
        ip_addresses = set()

        firewalls = defaultdict(list)

        for project in context.projects:
            # Calculate firewall rules for each network
            for firewall in compute.firewalls.all(project.id, context.cache):

                if firewall.direction != compute.firewalls.RuleDirection.Ingress:
                    continue

                if not firewall.allowed:
                    continue

                # funky control flow
                for allow in firewall.allowed:
                    if allow['IPProtocol'] in {'all', 'tcp'}:
                        break
                else:
                    continue

                firewalls[firewall.network].append(firewall)

            for rule_list in firewalls.values():
                rule_list.sort(key=lambda x: x.priority, reverse=True)

        for project in context.projects:

            addresses = compute.addresses.all(project.id, context.cache)

            for address in addresses:
                ip_addresses.add(IPAddress(address["address"]))

            instances = compute.instances.all(project.id, context.cache)

            for instance in instances:
                tags = set(instance["tags"].get("items", []))

                for interface in instance.get("networkInterfaces", []):

                    network = interface["network"]
                    network_ip = IPAddress(interface["networkIP"])

                    matching_rules = []

                    for rule in firewalls[network]:

                        in_rule = False

                        if rule.destination_ranges:
                            for dest in rule.destination_ranges:
                                if network_ip in dest:
                                    in_rule = True
                        
                        if rule.target_tags and (rule.target_tags & tags):
                            in_rule = True 

                        if in_rule:
                            if rule.source_ranges and '0.0.0.0/0' in rule.source_ranges:
                                print(f'Rule match: {rule}')
                                matching_rules.append(rule)


                    for config in interface.get("accessConfigs", {}):
                        ip_address = config.get("natIP")
                        if matching_rules and ip_address:
                            ip_address = IPAddress(ip_address)
                            ip_addresses.add(ip_address)


        ip_addresses = [addr for addr in ip_addresses if not addr.is_private()]
        ip_addresses = IPSet(ip_addresses)

        ranges = []
        for r in ip_addresses.iter_ipranges():
            ranges.extend(iprange_to_globs(r.first, r.last))
        ranges.sort()

        if ip_addresses:
            return self.finding(addresses=ranges)

@scan
class Something(Scan):
    """
    This scan does something.
    """

    @staticmethod
    def meta():
        return ScanMetadata("compute", "name",
                            "",
                            Severity.HIGH,
                            ["roles/iam.securityReviewer"])

    def run(self, context: Context) -> Optional[Finding]:
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
