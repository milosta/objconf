from typing import Optional, Callable, Any


class UNDEFINED:
    def __new__(cls, *args, **kwargs):
        raise NotImplementedError


class Attribute:
    """
    Attribute store the value in the owning class (Config) instance.
    Constructor has the following parameters:
    - ``type_``: The only required parameter - type of the attribute
        (`bool`, `str`, `int`, `list`(if supported), …).
        It is a callable that converts the value to the correct type.
        Some types might not be supported; e.g. the Python ini-like format
        does not support lists by default.
    - ``default``: Default value to use if not present in a configuration file.
    - ``key``: Specify key in configuration file if different from attribute name.
    - ``validator``: Callable that takes the configuration value and checks whether
        it is valid - return `True`, or not - return `False`.
    - ``transformer``: Transform the value from configuration file. This happens
        after the type conversion but before the validation.
        Can be used for example for transforming paths
        (expanding user home dire, changing relative paths to absolute, …).
    """
    PREFIX = 'objconf_'

    __slots__ = ('type_', 'default', 'key', 'validator', 'transformer', 'name', 'storage_name')

    def __init__(self,
                 type_: Callable[[Any], Any],
                 default: Any = UNDEFINED,
                 key: Optional[str] = None,
                 validator: Optional[Callable[[Any], bool]] = None,
                 transformer: Optional[Callable[[Any], Any]] = None):
        self.type_ = type_
        self.default = default
        self.key = key
        self.validator = validator
        self.transformer = transformer
        self.name = None
        self.storage_name = None

    def __set_name__(self, owner, name):
        self.name = name
        if self.key is None:
            self.key = name
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

    def type_conversion(self, value: Any) -> Any:
        return self.type_(value)
