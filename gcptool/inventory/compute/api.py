from gcptool.creds import credentials
from googleapiclient.discovery import build

client = build("compute", "v1", credentials=credentials)

# pylint: disable=no-member
addresses = client.addresses()

# pylint: disable=no-member
instances = client.instances()

# pylint: disable=no-member
zones = client.zones()

