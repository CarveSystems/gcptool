import enum

from dataclasses import dataclass, fields
from typing import Any, List, Optional

from gcptool.inventory.iam.policy import Policy

from gcptool.util import parse_dataclass
from ..cache import Cache, with_cache
from . import api


@dataclass
class Topic:
    name: str
    labels: dict
    message_storage_policy: dict
    kms_key_name: str
    schema_settings: dict
    sanitize_pzs: bool


@with_cache("pubsub", "topics")
def __list(project_id: str):
    response = api.topics.list(project=f'projects/{project_id}').execute()
    return response.get("topics", [])

def list(project_id: str, cache: Cache) -> List[Any]:

    raw_topics = __list(cache, project_id)

    return [parse_dataclass(topic, Topic) for topic in raw_topics]

@with_cache("iam", "pubsub")
def __get_iam_policy(topic_name: str):
    return api.topics.getIamPolicy(resource=topic_name).execute()

def get_iam_policy(topic_name: str, cache: Cache) -> Policy:
    return parse_dataclass(__get_iam_policy(cache, topic_name), Policy)

