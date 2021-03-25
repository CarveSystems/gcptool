{% extends "base.md" %}
{% block body %}

%{c} consultants found several Kubernetes Engine clusters that did not have access control and hardening set according to Google's recommendations.

The following clusters allowed for basic authentication. Basic authentication allows users and services to connect to a Kubernetes cluster using a username and password. Disabling this option, along with client certificate-based authentication, is recommended by Google in order to force authentication via the stronger IAM based authentication.

| Project | Cluster Name |
|:--------|:-------------|
{% for project in instances %}
{% for cluster in instances[project]["basic"] %}
| {{ project}} | {{ cluster }} |
{% endfor %}
{% endfor %}


The following clusters had legacy authorization enabled. Enabling the legacy authorization option enables attribute-based access control (ABAC) for the cluster. Google recommends that clusters running on Kubernetes Engine migrate to use the role-based access control (RBAC) instead.

| Project | Cluster Name |
|:--------|:-------------|
{% for project in instances %}
{% for cluster in instances[project]["legacy"] %}
| {{ project}} | {{ cluster }} |
{% endfor %}
{% endfor %}


The following clusters did not have Network Policy enforcement enabled. With enforcement enabled, fine-grained policies can be defined to restrict network activity to and from pods within a Kubernetes cluster.

| Project | Cluster Name |
|:--------|:-------------|
{% for project in instances %}
{% for cluster in instances[project]["net"] %}
| {{ project}} | {{ cluster }} |
{% endfor %}
{% endfor %}


The following clusters did not have Pod Security Policy enforcement enabled. Defining a set of pod security policies and enabling enforcement allows cluster administrators to restrict the permissions of pods running within a cluster. Note that Pod Security Policies are deprecated as of Kubernetes 1.21 and will be removed in Kubernetes 1.25. <!-- probably not worth recommending this if it's going to be removed soon... but there's no good replacement still?! -->

| Project | Cluster Name |
|:--------|:-------------|
{% for project in instances %}
{% for cluster in instances[project]["psp"] %}
| {{ project}} | {{ cluster }} |
{% endfor %}
{% endfor %}


{% endblock %}
{% block recommendation %}
- If possible, disable basic authentication and legacy authorization to force the use of modern authentication schemes.
- Consider enabling pod security and network policy enforcement when possible, as these enable more fine-grained control over a cluster's security.
{% endblock %}