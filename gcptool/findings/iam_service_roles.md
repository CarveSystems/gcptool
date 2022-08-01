{% extends "base.md" %}
{% block body %}
Carve found user accounts with the `iam.serviceAccountUser` role at the project level.[^gcp_service_acct_role]

Granting the Service Account User role to a user for a project gives the user access to all service accounts in the project, including service accounts that may be created in the future. Users granted the Service Account User role on a service account can use it to indirectly access all the resources to which the service account has access.

The following user accounts were assigned the `iam.serviceAccountUser` role for certain projects:

{% for project, user in instances %}
- {{ project }}: {{ user }}
{% endfor %}

{% endblock %}
{% block recommendation %}
Ensure that assignment of the `iam.serviceAccountUser` role to each user account is appropriate. Consider assigning less expansive permissions.

[^gcp_service_acct_role]:https://cloud.google.com/iam/docs/service-accounts#user-role)
{% endblock %}
