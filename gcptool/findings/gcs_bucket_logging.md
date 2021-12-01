{% extends "base.md" %}

{% block body %}
%{c} found GCP storage buckets with access logging disabled.


The following buckets do not have access logging enabled:

{% for bucket in buckets %}
- {{ bucket }}
{% endfor %}

Logging allows for the examination of actions that have affected the state of objects in a storage bucket. It also reveals who has access data. Logging is an essential tool for determining how or whether a data breach has occurred.

{% endblock %}

{% block recommendation %}
Consider enabling access and storage logs for all buckets.
{% endblock %}