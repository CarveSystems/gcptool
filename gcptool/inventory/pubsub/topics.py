import enum
from typing import List

from ..cache import Cache, with_cache
from . import api
from .types import Policy, Topic


@with_cache("pubsub", "topics")
def __list(project_id: str):
    response = api.topics.list(project=f"projects/{project_id}").execute()
    return response.get("topics", [])


def list(project_id: str, cache: Cache) -> List[Topic]:

    raw_topics = __list(cache, project_id)

    return [Topic(**topic) for topic in raw_topics]


@with_cache("iam", "pubsub")
def __get_iam_policy(topic_name: str):
    return api.topics.getIamPolicy(resource=topic_name).execute()


def get_iam_policy(topic_name: str, cache: Cache) -> Policy:
    return Policy(**__get_iam_policy(cache, topic_name))
