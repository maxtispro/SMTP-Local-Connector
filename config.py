from dataclasses import dataclass
import json
import types
from typing import Any

import yaml


@dataclass
class Local:
    domain: str
    hostname: str
    port: int

@dataclass
class Remote:
    domain: str
    hostname: str
    port: int
    from_email: str
    user: str
    secret: str

@dataclass
class Test:
    to_email: str

@dataclass
class Config:
    local: Local
    remote: Remote
    test: Test


with open("config.yaml") as stream:
    try:
        global config
        def load_object(obj: dict[Any, Any]):
            return types.SimpleNamespace(**obj)
        with open("config.yaml") as stream:
            obj = yaml.safe_load(stream)
        config: Config = json.loads(json.dumps(obj), object_hook=load_object)
    except yaml.YAMLError as exc:
        print(exc)