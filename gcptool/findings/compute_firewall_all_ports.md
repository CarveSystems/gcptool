{% extends "base.md" %}

{% block body %}

%{c} identified the following firewall rules allowing access to all ports.

{% for project in instances %}
{% for project_instance in instances[project] %}
- {{ project_instance.name }}
{% endfor %}
{% endfor %}
{% endblock %}

{% block recommendation %}
Review the firewall configuration. Restrict open ports to only those that are needed for application functionality.
{% endblock %}
