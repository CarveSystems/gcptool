{% extends "base.md" %}
{% block body %}

%{c} consultants found several buckets that were readable or writable by any user.

The following buckets were readable by any user:

{% for bucket in readable_buckets %}
- {{ bucket }}
{% endfor %}

The following buckets were world writable:

{% for bucket in writable_buckets %}
- {{ bucket }}
{% endfor %}

{% endblock %}
{% block recommendation %}
Review the list of buckets that have been exposed to the public. Disable this access in any case where it is unnecessary.
{% endblock %}
