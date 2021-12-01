{% extends "base.md" %}

{% block body %}

Several projects have firewall rules that allow ssh access from the Internet. 

In general, access to internal resources and administrative interfaces should be restricted to %{client}-controlled networks. The following %{app} projects have firewall rules that allow ssh access on port 22 from any IP (source range 0.0.0.0/0):

{% for project in instances %}
- {{ project }}
{% endfor %}

Note that 'default-allow-ssh' is a [pre-populated rule in the default network](https://cloud.google.com/vpc/docs/firewalls#more_rules_default_vpc) and may not have been deliberately enabled.

{% endblock %}

{% block recommendation %}

Only allow ssh access from IP addresses belonging to %{client}.

{% endblock %}