from gcptool.creds import credentials
from googleapiclient.discovery import build

client = build("compute", "v1", credentials=credentials)

# pylint: disable=no-member
addresses = client.addresses()

# pylint: disable=no-member
backend_buckets = client.backendBuckets()

# pylint: disable=no-member
backend_services = client.backendServices()

# pylint: disable=no-member
firewalls = client.firewalls()

# pylint: disable=no-member
forwarding_rules = client.forwardingRules()

# pylint: disable=no-member
instances = client.instances()

# pylint: disable=no-member
network_endpoint_groups = client.networkEndpointGroups()

# pylint: disable=no-member
regions = client.regions()

# pylint: disable=no-member
ssl_certs = client.sslCertificates()

# pylint: disable=no-member
ssl_policies = client.sslPolicies()

# pylint: disable=no-member
target_http_proxies = client.targetHttpProxies()

# pylint: disable=no-member
target_https_proxies = client.targetHttpsProxies()

# pylint: disable=no-member
target_ssl_proxies = client.targetSslProxies()

# pylint: disable=no-member
target_tcp_proxies = client.targetTcpProxies()

# pylint: disable=no-member
vpn_gateways = client.vpnGateways()

# pylint: disable=no-member
zones = client.zones()

