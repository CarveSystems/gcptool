from googleapiclient.discovery import build

from gcptool.creds import credentials

client = build("pubsub", "v1", credentials=credentials)

# pylint: disable=no-member
topics = client.projects().topics()