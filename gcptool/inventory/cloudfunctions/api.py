from gcptool.creds import credentials
from googleapiclient.discovery import build

client = build("cloudfunctions", "v1", credentials=credentials)

# pylint: disable=no-member
functions = client.projects().locations().functions()