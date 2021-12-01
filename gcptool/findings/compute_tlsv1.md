{% extends "base.md" %}
{% block body %}
HTTPS load balancers used by the %{app} used the default SSL policy, which allows for the TLS version 1.0 protocol. Due to its backwards compatibility with SSLv3, this protocol suffers from a number of cryptographic issues. Support for weak SSL protocols and inadequate underlying ciphers may result in the attacker performing a man-in-the-middle attack and defeating the encryption of a user's connection due to insufficient strength of the cipher or the cryptographic vulnerabilities identified in the protocol.

It should also be noted that as of June 30, 2018, TLS version 1.0 is considered insecure by the PCI standard.

%{c} identified the following GCP resources with vulnerable HTTPS servers running on port 443:

{% for project in instances %}
{% for lb, rule in instances[project] %}
- {{lb.name}} - {{ rule.ip_address }}
{% endfor %}
{% endfor %}


{% endblock %}
{% block recommendation %}
Where feasible, migrate fully to at least TLS version 1.1, disabling support for all SSL (both versions 2 and 3) cipher suites. Ensure that the key length is at least 128 bit for all supported ciphers. Do not support RC4-based cipher suites.

Only support strong cipher-suites. %{c} recommends defining a [SSL policy](https://cloud.google.com/load-balancing/docs/ssl-policies-concepts) that only allows for TLS version 1.1 or higher. Additionally, %{c} recommends using the `modern` or `restricted` pre-configured profiles when possible.
{% endblock %}