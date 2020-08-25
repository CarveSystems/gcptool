from googleapiclient.discovery import build

from gcptool.creds import credentials

client = build("cloudresourcemanager", "v1", credentials=credentials)

# TODO - GCP has a proper Python API client for the Resource Manager API.
# We don't really need any of the features it provides (we run read only)
# So, decide if we should just stick with this or run however we'd like.

# pylint: disable=no-member
projects = client.projects()
