import functools
import json
from pathlib import Path
from typing import Any, Callable, Dict, Optional


class Cache:
    """
    Simple class for storing raw GCP API responses to disk.
    """

    VERSION = 1

    def __init__(self, filename: Path, force: bool = False):
        self.filename = filename
        self.force = force

        if self.filename.exists():
            with self.filename.open("r") as f:
                self.data: Dict[str, Dict[str, Dict[str, Any]]] = json.load(f)

            # We store a meta
            if self.get("meta", "gcptool", "version") != self.VERSION:
                raise RuntimeError("Cache file version does not match tool version!")
        else:
            # The file doesn't exist. Just set it up with defaults for now.
            self.data = {}
            self.store("meta", "gcptool", "version", self.VERSION)

    def save(self):
        """
        Write the cache to disk.
        """

        # We don't want to accidentally leave a half-written file in place,
        # so write out to a temporary file and then replace the good one.

        tmp_filename = self.filename.with_suffix(".tmp")

        with tmp_filename.open("w") as f:
            json.dump(self.data, f, indent=2)

        tmp_filename.replace(self.filename)

    def get(self, service: str, resource: str, project: str) -> Optional[Any]:
        service_data = self.data.get(service)

        if not service_data:
            if self.force:
                raise IndexError(f"Cache-only mode requested, but {service} not found")
            return None

        resource_data = service_data.get(resource)

        if not resource_data:
            if self.force:
                raise IndexError(f"Cache-only mode requested, but {service}:{resource} not found")
            return None

        return resource_data.get(project)

    def store(self, service: str, resource: str, project: str, data: Any):
        service_data = self.data.get(service)

        if not service_data:
            service_data = {}
            self.data[service] = service_data

        resource_data = service_data.get(resource)
        if not resource_data:
            resource_data = {}
            service_data[resource] = resource_data

        resource_data[project] = data


def with_cache(
    service: str, resource: str
) -> Callable[[Callable[[str], Any]], Callable[[Cache, str], Any]]:
    """
    A decorator to automagically add support for caching to "simple" listing API calls.
    """

    def decorator(func: Callable[[str], Any]) -> Callable[[Cache, str], Any]:
        def wrapper_func(cache: Cache, item_id: str) -> Any:
            cached_data = cache.get(service, resource, item_id)

            if not cached_data:
                data = func(item_id)
                cache.store(service, resource, item_id, data)

                return data
            else:
                return cached_data

        return wrapper_func

    return decorator


_simple_cache = {}


def parse_model_cache(data: Any, model: Any) -> Any:
    # TODO -> LRU
    name = data["name"]
    if name in _simple_cache:
        return _simple_cache[name]
    else:
        obj = model(**data)
        _simple_cache[name] = obj
        return obj
