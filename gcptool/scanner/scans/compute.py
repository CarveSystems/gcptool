from collections import defaultdict
from os import stat
from typing import Any, Dict, List, Optional

from netaddr import IPAddress, IPSet, iprange_to_globs

import gcptool.inventory.compute as compute
from gcptool.inventory.compute import firewalls, target_https_proxies
from gcptool.scanner.context import Context
from gcptool.scanner.finding import Finding, Severity
from gcptool.scanner.scan import Scan, ScanMetadata, scan


@scan
class ComputeInventory(Scan):
    """
    This scan generates an inventory of Compute resources as an INFO finding.
    """

    @staticmethod
    def meta():
        return ScanMetadata(
            "compute",
            "inventory",
            "Inventory of Compute Resources",
            Severity.INFO,
            ["roles/iam.securityReviewer"],
        )

    def run(self, context: Context) -> Optional[Finding]:
        for project in context.projects:
            # ensure that all data for compute gets into the cache
            zones = compute.zones.all(project.id, context.cache)
            regions = compute.regions.all(project.id, context.cache)
            addresses = compute.addresses.all(project.id, context.cache)
            instances = compute.instances.all(project.id, context.cache)
            backend_buckets = compute.backend_buckets.all(project.id, context.cache)
            backend_services = compute.backend_services.all(project.id, context.cache)
            vpn_gateways = compute.vpn_gateways.all(project.id, context.cache)
            firewalls = compute.firewalls.all(project.id, context.cache)
            forwarding_rules = compute.forwarding_rules.all(project.id, context.cache)
            network_endpoint_groups = compute.network_endpoint_groups.all(project.id, context.cache)
            ssl_certs = compute.ssl_certs.all(project.id, context.cache)
            ssl_policies = compute.ssl_policies.all(project.id, context.cache)
            target_http_proxies = compute.target_http_proxies.all(project.id, context.cache)
            target_https_proxies = compute.target_https_proxies.all(project.id, context.cache)
            target_ssl_proxies = compute.target_ssl_proxies.all(project.id, context.cache)
            target_tcp_proxies = compute.target_tcp_proxies.all(project.id, context.cache)

        return None


@scan
class IPAddressDump(Scan):
    @staticmethod
    def meta():
        return ScanMetadata(
            "compute",
            "allspotter",
            "Inventory of IP addresses",
            Severity.INFO,
            ["roles/iam.securityReviewer"],
        )

    def run(self, context: Context) -> Optional[Finding]:
        ip_addresses = set()

        firewalls: Dict[str, List[compute.firewalls.Firewall]] = defaultdict(list)

        for project in context.projects:
            # Calculate firewall rules for each network
            for firewall in compute.firewalls.all(project.id, context.cache):

                if firewall.direction != firewall.direction.ingress:
                    continue

                if not firewall.allowed:
                    continue

                # funky control flow
                for allow in firewall.allowed:
                    if allow.ip_protocol in {"all", "tcp"}:
                        break
                else:
                    continue

                firewalls[firewall.network].append(firewall)

            for rule_list in firewalls.values():
                rule_list.sort(key=lambda x: x.priority, reverse=True)

        for project in context.projects:

            addresses = compute.addresses.all(project.id, context.cache)

            for address in addresses:
                ip_addresses.add(IPAddress(address.address))

            instances = compute.instances.all(project.id, context.cache)

            for instance in instances:
                tags = instance.tags.items

                for interface in instance.network_interfaces:

                    network = interface.network
                    network_ip = IPAddress(interface.network_ip)

                    matching_rules = []

                    for rule in firewalls[network]:

                        in_rule = False

                        if rule.destination_ranges:
                            for dest in rule.destination_ranges:
                                if network_ip in dest:
                                    in_rule = True

                        if rule.target_tags and tags and (set(rule.target_tags) & set(tags)):
                            in_rule = True

                        if in_rule:
                            if rule.source_ranges and "0.0.0.0/0" in rule.source_ranges:
                                matching_rules.append(rule)

                    if interface.access_configs:
                        for config in interface.access_configs:
                            ip_address = config.nat_ip
                            if matching_rules and ip_address:
                                ip_address = IPAddress(ip_address)
                                ip_addresses.add(ip_address)

        for project in context.projects:
            for rule in compute.forwarding_rules.all(project.id, context.cache):
                if rule.load_balancing_scheme == rule.load_balancing_scheme.external:
                    ip_addresses.add(IPAddress(rule.ip_address))

        ip_addresses = [addr for addr in ip_addresses if not addr.is_private()]
        ip_addresses = IPSet(ip_addresses)

        ranges = []
        for r in ip_addresses.iter_ipranges():
            ranges.extend(iprange_to_globs(r.first, r.last))
        ranges.sort()

        if ip_addresses:
            return self.finding(addresses=ranges)


@scan
class LoadBalancerTLSv1(Scan):
    @staticmethod
    def meta() -> ScanMetadata:
        return ScanMetadata(
            "compute",
            "tlsv1",
            "Load Balancers allow TLsv1.0 connections",
            Severity.LOW,
            ["roles/iam.securityReviewer"],
        )

    def run(self, context: Context) -> Optional[Finding]:

        instances = {}

        for project in context.projects:

            project_instances = []

            project_policies = compute.ssl_policies.all(project.id, context.cache)
            project_rules = compute.forwarding_rules.all(project.id, context.cache)

            policies_by_url: Dict[str, compute.ssl_policies.SslPolicy] = {
                p.self_link: p for p in project_policies
            }
            rules_by_target: Dict[str, compute.forwarding_rules.ForwardingRule] = {
                r.target: r for r in project_rules
            }

            for proxy in compute.target_https_proxies.all(project.id, context.cache):
                policy = proxy.ssl_policy

                if not policy:
                    # No defined policy means we're using the default
                    project_instances.append((proxy, rules_by_target.get(proxy.self_link)))
                    continue

                policy = policies_by_url[policy]

                if policy.min_tls_version == policy.min_tls_version.tls_1_0:
                    project_instances.append((proxy, rules_by_target.get(proxy.self_link)))

            for proxy in compute.target_ssl_proxies.all(project.id, context.cache):
                policy = proxy.ssl_policy

                if not policy:
                    # No defined policy means we're using the default
                    project_instances.append((proxy, rules_by_target.get(proxy.self_link)))
                    continue

                policy = policies_by_url[policy]

                if policy.min_tls_version == policy.min_tls_version.tls_1_0:
                    project_instances.append((proxy, rules_by_target.get(proxy.self_link)))

            if project_instances:
                instances[project.name] = project_instances

        if instances:
            return self.finding(instances=instances)


@scan
class LoadBalancerHttp(Scan):
    @staticmethod
    def meta() -> ScanMetadata:
        return ScanMetadata(
            "compute",
            "http",
            "Load Balancers allow plaintext HTTP connections",
            Severity.LOW,
            ["roles/iam.securityReviewer"],
        )

    def run(self, context: Context) -> Optional[Finding]:

        instances = {}

        for project in context.projects:

            project_instances = []

            project_rules = compute.forwarding_rules.all(project.id, context.cache)

            rules_by_target: Dict[str, compute.forwarding_rules.ForwardingRule] = {
                r.target: r for r in project_rules
            }

            for proxy in compute.target_http_proxies.all(project.id, context.cache):
                rule = rules_by_target.get(proxy.self_link)

                if rule.load_balancing_scheme == rule.load_balancing_scheme.external:
                    project_instances.append((proxy, rules_by_target.get(proxy.self_link)))

            if project_instances:
                instances[project.name] = project_instances

        if instances:
            return self.finding(instances=instances)


@scan
class InternalTrafficFirewall(Scan):
    @staticmethod
    def meta() -> ScanMetadata:
        return ScanMetadata(
            "compute",
            "firewall_internal",
            "firewall_internal",
            Severity.LOW,
            ["roles/iam.securityReviewer"],
        )

    def run(self, context: Context) -> Optional[Finding]:
        matches = {}

        for project in context.projects:

            project_matches = []

            for firewall in compute.firewalls.all(project.id, context.cache):

                if not firewall.allowed:
                    continue

                if firewall.disabled:
                    continue

                if firewall.direction != firewall.direction.ingress:
                    continue

                for item in firewall.allowed:
                    if item.ports and ("0-65535" in item.ports or "1-65535" in item.ports):
                        break
                else:
                    continue

                if "10.128.0.0/9" in firewall.source_ranges:
                    project_matches.append(firewall)

            if project_matches:
                matches[project.id] = project_matches

        if matches:
            return self.finding(instances=matches)


@scan
class InternalTrafficFirewall(Scan):
    @staticmethod
    def meta() -> ScanMetadata:
        return ScanMetadata(
            "compute",
            "firewall_all_ports",
            "Firewall rule allows all ports",
            Severity.LOW,
            ["roles/iam.securityReviewer"],
        )

    def run(self, context: Context) -> Optional[Finding]:
        matches = {}

        for project in context.projects:

            project_matches = []

            for firewall in compute.firewalls.all(project.id, context.cache):

                if not firewall.allowed:
                    continue

                if firewall.disabled:
                    continue

                if firewall.direction != firewall.direction.ingress:
                    continue

                for item in firewall.allowed:
                    if item.ports and ("0-65535" in item.ports or "1-65535" in item.ports):
                        break
                else:
                    continue

                project_matches.append(firewall)

            if project_matches:
                matches[project.id] = project_matches

        if matches:
            return self.finding(instances=matches)


@scan
class FirewallAllowsRDP(Scan):
    @staticmethod
    def meta() -> ScanMetadata:
        return ScanMetadata(
            "compute", "firewall_rdp", "firewall_rdp", Severity.LOW, ["roles/iam.securityReviewer"]
        )

    def run(self, context: Context) -> Optional[Finding]:
        matches = {}

        for project in context.projects:

            project_matches = []

            for firewall in compute.firewalls.all(project.id, context.cache):

                if firewall.disabled:
                    continue

                if firewall.name == "default-allow-rdp":
                    project_matches.append(firewall)

            if project_matches:
                matches[project.id] = project_matches

        if matches:
            return self.finding(instances=matches)


class FirewallAllowsSSH(Scan):
    @staticmethod
    def meta() -> ScanMetadata:
        return ScanMetadata(
            "compute", "firewall_ssh", "firewall_ssh", Severity.LOW, ["roles/iam.securityReviewer"]
        )

    def run(self, context: Context) -> Optional[Finding]:
        matches = {}

        for project in context.projects:

            project_matches = []

            for firewall in compute.firewalls.all(project.id, context.cache):

                if firewall.disabled:
                    continue

                if firewall.name == "default-allow-ssh":
                    project_matches.append(firewall)

            if project_matches:
                matches[project.id] = project_matches

        if matches:
            return self.finding(instances=matches)


@scan
class FirewallPublic(Scan):
    @staticmethod
    def meta() -> ScanMetadata:
        return ScanMetadata(
            "compute",
            "firewall_public",
            "Firewall rule allows public traffic",
            Severity.LOW,
            ["roles/iam.securityReviewer"],
        )

    def run(self, context: Context) -> Optional[Finding]:

        matches = {}

        for project in context.projects:

            project_matches = []

            for firewall in compute.firewalls.all(project.id, context.cache):

                if firewall.disabled:
                    continue

                if firewall.direction != firewall.direction.ingress:
                    continue

                if not firewall.allowed:
                    continue

                if "0.0.0.0/0" in firewall.source_ranges:
                    project_matches.append(firewall)

            if project_matches:
                matches[project.id] = project_matches

        if matches:
            return self.finding(instances=matches)


@scan
class Something(Scan):
    """
    This scan does something.
    """

    @staticmethod
    def meta():
        return ScanMetadata("compute", "name", "", Severity.HIGH, ["roles/iam.securityReviewer"])

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
