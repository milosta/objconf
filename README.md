# Objconf - Object Configuration for Python
[![Build Status](https://app.travis-ci.com/milosta/objconf.svg?branch=master)](https://app.travis-ci.com/milosta/objconf)
## What is objconf?
Objconf provides object configuration for Python.
It allows accessing the configuration values as attributes of a configuration object.

Unlike Python built-in configparser, all values have a type. Objconf also supports transformation
and validation of values. For example, you can tell objconf to transform relative path to absolute
and verify that the file exists.

Here is an example of what would this simple configuration object look like:

```python
import objconf, os

class AppConfig(objconf.Config):
    key_path = objconf.Attribute(
        str,
        transformer=lambda x: os.path.abspath(x),
        validator=lambda x: os.path.isfile(x))
```

Supported configuration formats:
- YAML
- JSON
- Python ini-like configparser format


## Installation
Objconf can be installed using pip:
```bash
python3 -m pip install objconf 
```

## Documentation

### Config class
`Config` is a base class for your configuration class.
Inherit from this class when defining your application configuration.
```python
from objconf import Config, Attribute


class AppConfig(Config):
    string_attr = Attribute(str)
    int_attr = Attribute(int, default=5)


with open('config.yaml') as f:  # Similarly for other configuration formats
    app_config = AppConfig.load_yaml
```

#### Loading configuration
The configuration is loaded during creation of the `Config` subclass instance specifying
the configuration values for your application. The instance is created by the factory
methods `load_*`.

They all take `stream` parameter which is a file-like object with configuration values
in the corresponding format. (Except `load_dict`, it takes a dictionary
and  all other loading methods use it internally.)
Another common parameter is `extra_vals` that specify behavior when encountering
an unspecified attribute in the configuration.

The loading functions take also other arguments specific for the format and modifying
the behaviour of underlying parser.

``load_yaml`` - Load configuration from YAML

``load_json`` - Load configuration from JSON

``load_ini`` - Load configuration from python ini-like configparser format


### Attributes
Attribute store the value in the owning class (Config) instance.
Constructor has the following parameters:
- ``type_``: The only required parameter - type of the attribute
    (`str`, `int`, `list`(if supported), …).
    It is a callable that converts the value to the correct type.
    Some types might not be supported; e.g. the Python ini-like format
    does not support lists by default.
- ``default``: Default value to use if not present in a configuration file.
- ``key``: Specify key in configuration file if different from attribute name.
- ``validator``: Callable that takes the configuration value and checks whether 
    it is valid - return `True`, or not - return `False`.
- ``transformer``: Transform the value from configuration file. This happens before
    the validation. Can be used for example for transforming paths
    (expanding user home dire, changing relative paths to absolute, …).

## Tests
Objconf uses tox to run the tests.
```bash
python3 -m pip install tox
python3 -m tox
```
