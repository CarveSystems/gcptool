{% extends "base.md" %}
{% block body %}

%{c} consultants found Google Cloud Functions functions that could be triggered by any user.


{% for project in instances %}
  {% for function in instances[project] %}
- {{ function.name }}: {{ function.https_trigger.url }}
  {% endfor %}
{% endfor %}

{% endblock %}
{% block recommendation %}
Review the list of triggerable functions. Ensure that none of them expose sensitive functionality without authentication.
{% endblock %}
