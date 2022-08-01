{% extends "base.md" %}

{% block body %}
%{c} found service accounts with user managed keys.
User-managed keys are extremely powerful credentials, and they can represent a security risk if they are not managed correctly. It is the responsibility of the user to ensure that appropriate security practices are followed and that keys remain secure.

The following service accounts were found to make use of user-managed keys:

{% for project in instances %}
{% for account in instances[project] %}
- {{ account }}
{% endfor %}
{% endfor %}

{% endblock %}

{% block recommendation %}
Consider using [Cloud Key Management Service (Cloud KMS)](https://cloud.google.com/kms/docs) to help securely manage your keys.

You can limit the use of user-managed service keys by applying the `constraints/iam.disableServiceAccountKeyCreation` Organization Policy Constraint to projects, folders, or even your entire organization. After applying the constraint, you can enable user-managed keys in well-controlled locations to minimize the potential risk caused by unmanaged keys.[^gcp_userkeys]

[^gcp_userkeys]:[Cloud IAM -- Service Accounts -- Preventing User Managed Keys](https://cloud.google.com/iam/docs/service-accounts#preventing_user-managed_keys)`
{% endblock %}
