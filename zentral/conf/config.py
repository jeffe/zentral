import base64
import itertools
import json
import logging
import re
import os


logger = logging.getLogger("zentral.conf.config")


class Proxy:
    pass


class EnvProxy(Proxy):
    def __init__(self, name):
        self._value = os.environ[name]

    def get(self):
        return self._value


class FileProxy(Proxy):
    def __init__(self, filepath):
        self._filepath = filepath

    def get(self):
        with open(self._filepath, "r") as f:
            return f.read()


class JSONDecodeProxy(Proxy):
    def __init__(self, child_proxy):
        self._child_proxy = child_proxy

    def get(self):
        return json.loads(self._child_proxy.get())


class Base64DecodeProxy(Proxy):
    def __init__(self, child_proxy):
        self._child_proxy = child_proxy

    def get(self):
        return base64.b64decode(self._child_proxy.get())


class BaseConfig:
    PROXY_VAR_RE = re.compile(
        r"^\{\{\s*"
        r"(?P<type>env|file)\:(?P<key>[^\}\|]+)"
        r"(?P<filters>(\s*\|\s*(jsondecode|base64decode))*)"
        r"\s*\}\}$"
    )
    custom_classes = {}

    @staticmethod
    def _make_proxy(key, match):
        proxy_type = match.group("type")
        proxy_key = match.group("key").strip()
        if proxy_type == "env":
            proxy = EnvProxy(proxy_key)
        elif proxy_type == "file":
            proxy = FileProxy(proxy_key)
        else:
            raise ValueError("Unknown proxy type {}".format(proxy_type))
        filters = [f for f in [rf.strip() for rf in match.group("filters").split("|")] if f]
        for filter_name in filters:
            if filter_name == "jsondecode":
                proxy = JSONDecodeProxy(proxy)
            elif filter_name == "base64decode":
                proxy = Base64DecodeProxy(proxy)
        return proxy

    def _from_python(self, key, value):
        new_path = self._path + (key,)
        if isinstance(value, dict):
            value = self.custom_classes.get(new_path, ConfigDict)(value, new_path)
        elif isinstance(value, list):
            value = self.custom_classes.get(new_path, ConfigList)(value, new_path)
        elif isinstance(value, str):
            match = self.PROXY_VAR_RE.match(value)
            if match:
                value = self._make_proxy(key, match)
        return value

    def _to_python(self, value):
        if isinstance(value, Proxy):
            return value.get()
        else:
            return value

    def __iter__(self):
        return self._collection.__iter__()

    def __len__(self):
        return len(self._collection)

    def __delitem__(self, key):
        del self._collection[key]

    def __setitem__(self, key, value):
        self._collection[key] = self._from_python(key, value)

    def pop(self, key, default=None):
        value = self._collection.pop(key, default)
        if isinstance(value, Proxy):
            value = value.get()
        return value


class ConfigList(BaseConfig):
    def __init__(self, config_l, path=None):
        self._path = path or ()
        self._collection = []
        for key, value in enumerate(config_l):
            self._collection.append(self._from_python(str(key), value))

    def __getitem__(self, key):
        value = self._collection[key]
        if isinstance(key, slice):
            slice_repr = ":".join(str("" if i is None else i) for i in (key.start, key.stop, key.step))
            logger.debug("Get /%s[%s] config key", "/".join(self._path), slice_repr)
            return [self._to_python(item) for item in value]
        else:
            logger.debug("Get /%s[%s] config key", "/".join(self._path), key)
            return self._to_python(value)


class ConfigDict(BaseConfig):
    def __init__(self, config_d, path=None):
        self._path = path or ()
        self._collection = {}
        for key, value in config_d.items():
            self._collection[key] = self._from_python(key, value)

    def __getitem__(self, key):
        logger.debug("Get /%s config key", "/".join(self._path + (key,)))
        value = self._collection[key]
        return self._to_python(value)

    def get(self, key, default=None):
        try:
            value = self[key]
        except KeyError:
            value = self._to_python(default)
        return value

    def keys(self):
        return self._collection.keys()

    def values(self):
        for value in self._collection.values():
            yield self._to_python(value)

    def items(self):
        for key, value in self._collection.items():
            yield key, self._to_python(value)

    def clear(self):
        return self._collection.clear()

    def setdefault(self, key, default=None):
        return self._collection.setdefault(key, self._from_python(key, default))

    def pop(self, key, default=None):
        value = self._collection.pop(key, default)
        return self._to_python(value)

    def popitem(self):
        key, value = self._collection.popitem()
        return key, self._to_python(value)

    def copy(self):
        return self._collection.copy()

    def update(self, *args, **kwargs):
        chain = []
        for arg in args:
            if isinstance(arg, dict):
                iterator = arg.items()
            else:
                iterator = arg
            chain = itertools.chain(chain, iterator)
        if kwargs:
            chain = itertools.chain(chain, kwargs.items())
        for key, value in iterator:
            self._collection[key] = self._from_python(key, value)