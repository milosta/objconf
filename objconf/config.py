import configparser
import inspect
import json
import warnings
from enum import Enum, auto
from typing import Dict, Set, TextIO, Any, Optional, Iterable

import yaml

from objconf import attributes


class ExtraVals(Enum):
    IGNORE = auto()
    WARNING = auto()
    ERROR = auto()


class Config:
    @classmethod
    def from_yaml(cls, stream: TextIO, loader=yaml.SafeLoader,
                  extra_vals: ExtraVals = ExtraVals.WARNING) -> 'Config':
        return cls.from_dict(yaml.load(stream, loader), extra_vals)

    @classmethod
    def from_json(cls, stream: TextIO, extra_vals: ExtraVals = ExtraVals.WARNING,
                  **parser_kwargs) -> 'Config':
        return cls.from_dict(json.load(stream, **parser_kwargs), extra_vals)

    @classmethod
    def from_ini(cls, stream: TextIO, sections: Optional[Iterable[str]] = None,
                 extra_vals: ExtraVals = ExtraVals.WARNING, **parser_kwargs) -> 'Config':
        cfgparser = configparser.ConfigParser(**parser_kwargs)
        cfgparser.read_file(stream)
        if sections is None:
            sections = cfgparser.sections()
        data = {}  # type: Dict[str, Any]
        for section in sections:
            data.update(cfgparser[section])

        return cls.from_dict(data, extra_vals)

    @classmethod
    def from_dict(cls, data: Dict[str, Any], extra_vals: ExtraVals = ExtraVals.WARNING) -> 'Config':
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
    def handle_extra_vals(action: ExtraVals, extras: Set[str]) -> None:
        if action == ExtraVals.IGNORE:
            return
        msg = f'Found unrecognised configuration values: {extras}'
        if action == ExtraVals.WARNING:
            warnings.warn(msg)
            return
        if action == ExtraVals.ERROR:
            raise ValueError(msg)
