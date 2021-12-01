{% extends "base.md" %}

{% block body %}

Several projects have firewall rules that allow Microsoft Remote Desktop Protocol (RDP) access from the Internet. 

In general, access to internal resources and administrative interfaces should be restricted to %{client}-controlled networks. The following %{app} projects have firewall rules that allow RDP access on port 3389 from any IP (source range 0.0.0.0/0):

{% for project in instances %}
- {{ project }}
{% endfor %}

Note that 'default-allow-rdp' is a [pre-populated rule in the default network](https://cloud.google.com/vpc/docs/firewalls#more_rules_default_vpc) and may not have been deliberately enabled.

{% endblock %}

{% block recommendation %}

The default firewall rule 'default-allow-rdp' should be disabled everywhere. If needed, only allow RDP access from IP addresses belonging to %{client}.

{% endblock %}