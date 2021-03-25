{% extends "base.md" %}
{% block body %}
%{c} found service account credentials that had not been rotated in over 100 days.

Generally, the longer an access key is valid the higher the risk of unauthorized access. The following accounts had access keys that were over 100 days old:

{% for project in instances %}
{% for account in instances[project] %}
- {{ account }}
{% endfor %}
{% endfor %}
{% endblock %}
{% block recommendation %}
Google recommends regularly rotating service account access keys used by external services. This can be done by adopting a process for periodic rotation of credentials that will help reduce the risk of unauthorized access to the service accounts associated with the credentials.
{% endblock %}