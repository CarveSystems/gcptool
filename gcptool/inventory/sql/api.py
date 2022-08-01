from googleapiclient.discovery import build

from gcptool.creds import credentials

client = build("sqladmin", "v1", credentials=credentials)

# pylint: disable=no-member
databases = client.databases()

# pylint: disable=no-member
instances = client.instances()

users = client.users()
