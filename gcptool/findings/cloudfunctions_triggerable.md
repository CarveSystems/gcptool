{% extends "base.md" %}
{% block body %}

%{c} consultants found Google Cloud Functions functions that could be triggered by any user.


{% for project in instances %}
  {% for function in instances[project] %}
- {{ function }}
  {% endfor %}
{% endfor %}

{% endblock %}
{% block recommendation %}
We can put in some recommendation text here.
{% endblock %}
