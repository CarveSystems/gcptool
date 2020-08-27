from googleapiclient.discovery import build

from gcptool.creds import credentials

client = build("iam", "v1", credentials=credentials)

# pylint: disable=no-member
roles = client.roles()

