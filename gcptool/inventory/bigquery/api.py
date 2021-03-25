from gcptool.creds import credentials
from googleapiclient.discovery import build

client = build("bigquery", "v2", credentials=credentials)

# pylint: disable=no-member
datasets = client.datasets()

# pylint: disable=no-member
tables = client.tables()
