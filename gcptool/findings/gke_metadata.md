{% extends "base.md" %}
{% block body %}
The Kubernetes Engine clusters in use did not protect against access to instance metadata.

When a new Kubelet node is deployed on Kubernetes Engine, configuration options are passed to the new node via the `kube-env` variable of the node's [instance metadata.](https://cloud.google.com/compute/docs/storing-retrieving-metadata) This variable includes keys used for authenticating the node with the master API. As a result, access to these credentials, provided by a vulnerability in a pod deployed to a node, could allow an attacker to impersonate the node.

Additionally, the metadata service allows for the retrieval of credentials for the service account assigned to the node a Kubernetes pod is running on.

The following clusters did not protect their instance metadata:

| Project | Cluster Name |
|:--------|:-------------|
{% for project in instances %}
{% for cluster in instances[project]["all"] %}
| {{ project }} | {{ cluster.name }} |
{% endfor %}
{% endfor %}

The following clusters did not protect instance metadata, allowed API access to all Google Cloud APIs, and used a high-privileged service account. This combination would allow compromise of a running pod to lead to compromise of the containing project:

| Project | Cluster Name | IAM User |
|:--------|:-------------|:---------|
{% for project in instances %}
{% for cluster in instances[project]["high_privilege"] %}
| {{ project }} | {{ cluster.name }} | {{ service_accounts[cluster.name] }} |
{% endfor %}
{% endfor %}

{% endblock %}
{% block recommendation %}
[Workload Identity](https://cloud.google.com/kubernetes-engine/docs/how-to/workload-identity) can be used to assign a service account to each separate workload running in a cluster. While currently in beta, this feature prevents workloads from accessing node metadata, and allows for finer-grained control than assigning a service account to each node.
{% endblock %}
