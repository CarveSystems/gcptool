{% extends "base.md" %}
{% block body %}
Cloud SQL instances were configured with publicly accessible IP addresses and did not enforce TLS connections.

The following cloud SQL databases did not enforce TLS connections:

{% for project in vulnerable_projects %}
Instances in {{ project }}:

{% for instance in vulnerable_projects[project] %}
- {{ instance.name }}
{% endfor %}

{% endfor %}

Note that this excludes any Cloud SQL instances that do not also configure a set of authorized networks. Such instances are typically accessed via the Cloud SQL proxy, and as the proxy will always use a TLS connection, TLS enforcement is not necessary to ensure a secure connection is used.
{% endblock %}
{% block recommendation %}
Enable TLS enforcement for all Cloud SQL databases with a public IP address to prevent any plaintext information from being sent over the internet.
{% endblock %}
