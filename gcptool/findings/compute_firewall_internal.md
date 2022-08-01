{% extends "base.md" %}

{% block body %}

Several projects have the 'default-allow-internal' firewall rule that allows unrestricted access from the local VPC subnet.

%{c} identified the following projects with the 'default-allow-internal' rule active:

{% for project in instances %}
- {{ project }}
{% endfor %}

Note that 'default-allow-internal' is a [pre-populated rule in the default network](https://cloud.google.com/vpc/docs/firewalls#more_rules_default_vpc) and may not have been deliberately enabled. This rule allows all traffic from hosts on the 10.128.0.0/9 subnet.


{% endblock %}

{% block recommendation %}
Review project configurations to ensure that appropriate internal network rules are in place.
{% endblock %}
