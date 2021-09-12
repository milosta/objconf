class UNDEFINED:
    def __new__(cls, *args, **kwargs):
        raise NotImplementedError


class Attribute:
    __slots__ = ('key', 'type_', 'storage_name', 'default', 'validator', 'transformer')
    PREFIX = 'objconf_'

    def __init__(self, key, type_, default=UNDEFINED, validator=None, transformer=None):
        self.key = key
        self.type_ = type_
        self.default = default
        self.validator = validator
        self.transformer = transformer
        self.storage_name = self.PREFIX + self.__name__

    def __set__(self, instance, value):
        value = self.type_conversion(value)
        if self.transformer:
            value = self.transformer(value)
        if self.validator and not self.validator(value):
            raise ValueError(f'The value "{value}" is not valid.')
        setattr(instance, self.storage_name, value)

    def __get__(self, instance):
        return getattr(instance, self.storage_name)

    def type_conversion(self, value):
        return self.type_(value)
