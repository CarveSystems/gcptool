from googleapiclient.discovery import build

from gcptool.creds import credentials

client = build("cloudfunctions", "v1", credentials=credentials)

# pylint: disable=no-member
functions = client.projects().locations().functions()
