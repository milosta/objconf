import inspect
import warnings
from enum import Enum, auto
from typing import Dict, Set

import yaml

from objconf import attributes


class ExtraVals(Enum):
    IGNORE = auto()
    WARNING = auto()
    ERROR = auto()


class Config:
    @classmethod
    def load_yaml(cls, stream, loader=yaml.SafeLoader, *args, **kwargs):
        return cls.load_from_dict(yaml.load(stream, loader), *args, **kwargs)

    @classmethod
    def load_from_dict(cls, data: Dict, extra_vals: ExtraVals = ExtraVals.WARNING):
        config = cls()
        data_keys = set(data.keys())

        for attr_name, attr in inspect.getmembers(
                cls, lambda x: isinstance(x, attributes.Attribute)):
            value = data.get(attr.key, attr.default)
            if value == attributes.UNDEFINED:
                raise RuntimeError(f'Missing required attribute {attr.key}')

            setattr(config, attr_name, value)
            data_keys.discard(attr.key)

        if data_keys:
            cls.handle_extra_vals(extra_vals, data_keys)
        return config

    @staticmethod
    def handle_extra_vals(action: ExtraVals, extras: Set) -> None:
        if action == ExtraVals.IGNORE:
            return
        msg = f'Found unrecognised configuration values: {extras}'
        if action == ExtraVals.WARNING:
            warnings.warn(msg)
            return
        if action == ExtraVals.ERROR:
            raise ValueError(msg)
