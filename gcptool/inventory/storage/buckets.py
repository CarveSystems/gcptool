from typing import List

from google.cloud import storage

from gcptool.creds import credentials

from gcptool.inventory.cache import Cache, with_cache

@with_cache("cloudstorage","buckets")
def __all(project: str):
    client = storage.Client(project=project, credentials=credentials)

    buckets = list(client.list_buckets(projection='full'))

    return [bucket._properties for bucket in buckets]



def all(project: str, cache: Cache) -> List[storage.Bucket]:

    client = storage.Client(project=project, credentials=credentials)
    raw_buckets = __all(cache, project)

    buckets = []


    for props in raw_buckets:
        bucket_name = props.get('name')
        bucket = storage.Bucket(client, bucket_name)
        bucket._set_properties(props)

        # For some reason, the Google client library doesn't load the ACL from the list response,
        # even if we ask it to load it ('full' projection includes the ACL).
        # As we may be running with restricted access (i.e, storage.buckets.list without storage.buckets.get),
        # letting the Google library lazy load the data later could fail.
        # So, we manually load it now.
        bucket.acl.loaded = True
        for item in bucket._properties.get('acl', []):
            bucket.acl.add_entity(bucket.acl.entity_from_dict(item))

        buckets.append(bucket)

    return buckets
