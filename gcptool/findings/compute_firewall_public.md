{% extends "base.md" %}

{% block body %}

<!-- TODO - review these  -->

%{c} identified the following firewall rules allowing access to all IP addresses.

{% for project in instances %}
{% for project_instance in instances[project] %}
- {{ project_instance.name }}
{% endfor %}
{% endfor %}
{% endblock %}

{% block recommendation %}
Review the firewall configuration. If any services are unnecessarily being made accessible, modify the rule to be as strict as possible.
{% endblock %}
