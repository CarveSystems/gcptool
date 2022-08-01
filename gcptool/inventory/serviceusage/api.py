from googleapiclient.discovery import build

from gcptool.creds import credentials

client = build("serviceusage", "v1", credentials=credentials)

services = client.services()
