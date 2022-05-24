{% extends "base.md" %}

{% block body %}

%{c} found GCP storage buckets with object versioning disabled.

Of the {{ total }} buckets identified for the %{app}, {{ affected }} were found to have versioning disabled.

The following buckets have object versioning disabled:

{% for bucket in buckets %}
- {{ bucket }}
{% endfor %}

Versioning allows for the the recovery of objects that have been deleted or overwritten. In the absence of object versioning, an attacker with appropriate access may be able to permanently delete data. Versioning also guards against accidental deletion.

{% endblock %}

{% block recommendation %}

Consider enabling object versioning for all buckets.

{% endblock %}