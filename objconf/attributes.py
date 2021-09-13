from collections import Callable


class UNDEFINED:
    def __new__(cls, *args, **kwargs):
        raise NotImplementedError


class Attribute:
    PREFIX = 'objconf_'

    __slots__ = ('key', 'type_', 'default', 'validator', 'transformer', 'name', 'storage_name')

    def __init__(self, key: str, type_: Callable, default=UNDEFINED, validator=None, transformer=None):
        self.key = key
        self.type_ = type_
        self.default = default
        self.validator = validator
        self.transformer = transformer
        self.name = None
        self.storage_name = None

    def __set_name__(self, owner, name):
        self.name = name
        self.storage_name = self.PREFIX + name

    def __set__(self, instance, value):
        value = self.type_conversion(value)
        if self.transformer:
            value = self.transformer(value)
        if self.validator and not self.validator(value):
            raise ValueError(f'The value "{value}" is not valid.')
        setattr(instance, self.storage_name, value)

    def __get__(self, instance, owner=None):
        if instance is None:
            return self
        return getattr(instance, self.storage_name)

    def type_conversion(self, value):
        return self.type_(value)
