import google.auth

# TODO - allow users to choose their own credentials.
# For now, we'll just use the default user the GCP CLI is authenticated with.

credentials, project = google.auth.default()
