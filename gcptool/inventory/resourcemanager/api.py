from googleapiclient.discovery import build

from gcptool.creds import credentials

client = build("cloudresourcemanager", "v1", credentials=credentials)

# pylint: disable=no-member
projects = client.projects()
