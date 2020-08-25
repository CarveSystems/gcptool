from typing import Dict

from google.cloud import storage

from gcptool.creds import credentials


def all(project: str):
    client = storage.Client(project=project, credentials=credentials)
    return list(client.list_buckets())
