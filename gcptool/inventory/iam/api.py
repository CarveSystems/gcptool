from googleapiclient.discovery import build

from gcptool.creds import credentials

client = build("iam", "v1", credentials=credentials)

# pylint: disable=no-member
roles = client.roles()

# pylint: disable=no-member
permissions = client.permissions()

# pylint: disable=no-member
service_accounts = client.projects().serviceAccounts()