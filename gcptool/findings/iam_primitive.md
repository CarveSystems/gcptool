{% extends "base.md" %}
{% block body %}

The %{app} Google Cloud environment used primitive IAM roles, including the assignment of the `editor` role to the default Compute Engine VM service account.

The primitive roles provided by Google Cloud Platform are generally overly broad, providing complete access to view or edit all resources in a project. This is particularly dangerous when applied to the Compute Engine default service account, as an application vulnerability may allow an attacker to retrieve an access token with excessive privileges.

The following list of users, groups, and service accounts were granted access editor, owner, or viewer access.

Entities with the `owner` role:

| Project | Entity |
|:--------|:-------|
{% for project in instances %}
{% for entity in instances[project]["owners"] %}
| {{ project }} | {{ entity }} |
{% endfor %}
{% endfor %}

Entities with the `editor` role:

| Project | Entity |
|:--------|:-------|
{% for project in instances %}
{% for entity in instances[project]["editors"] %}
| {{ project }} | {{ entity }} |
{% endfor %}
{% endfor %}

Entities with the `viewer` role:

| Project | Entity |
|:--------|:-------|
{% for project in instances %}
{% for entity in instances[project]["viewers"] %}
| {{ project }} | {{ entity }} |
{% endfor %}
{% endfor %}

{% endblock %}
{% block recommendation %}
The use of primitive roles should be minimized. Instead, a set of pre-defined or custom roles with the minimum access needed should be used.

In particular, the default service account for Compute Engine resources should be configured to be as strict as possible.
{% endblock %}