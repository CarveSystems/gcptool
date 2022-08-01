{% extends "base.md" %}

{% block body %}
The HTTP protocol was enabled for GKE external load balancers used by the %{app}. Clients using this protocol may transmit passwords and sensitive data in plaintext, which is trivial for an attacker with a vantage to perform a man-in-the-middle attack to intercept and manipulate.

%{c} identified the following GCP resources with HTTP servers running on port 80:

{% for project in instances %}
{% for proxy, rule in instances[project] %}
- {{ proxy.name }} - {{ rule.ip_address}}
{% endfor %}
{% endfor %}
{% endblock %}

{% block recommendation %}
Do not allow use of HTTP on port 80 for external load balancers in GKE. See [Ingress for External HTTP(S) Load Balancing -- Disabling HTTP](https://cloud.google.com/kubernetes-engine/docs/concepts/ingress-xlb#disabling_http).
{% endblock %}
