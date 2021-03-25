{% extends "base.md" %}
{% block body %}
Kubernetes Engine master nodes were accessible from the internet.

Kubernetes Engine clusters use a control plane that is hosted by Google separately from the Compute Engine VMs that make up the cluster. As a result, the firewall rules in place across the rest of the network do not apply to the master node, and the master node is accessible over the internet by default. While accessing the APIs hosted on the master node requires a secure connection and valid credentials, restricting access to the master node may make cluster compromise more difficult if valid credentials were to be leaked or if an authentication vulnerability were found.

The following clusters were found to have masters exposed to the internet:

| Project | Cluster | Master IP Address |
|:--------|:--------|:------------------|
{% for project in instances %}
{% for cluster in instances[project] %}
| {{ project }} || {{ cluster.name }} || {{ cluster.endpoint }} |
{% endfor %}
{% endfor %}
{% endblock %}

{% block recommendation %}
Set [authorized networks](https://cloud.google.com/kubernetes-engine/docs/how-to/authorized-networks) to restrict access to the master nodes to only allow access from IP addresses belonging to %{client}. Note that even with this option enabled, the master node is still accessible from within the Google Cloud.

Consider using [private clusters](https://cloud.google.com/kubernetes-engine/docs/how-to/private-clusters) when deploying new clusters in the future, to further minimize external access.
{% endblock %}