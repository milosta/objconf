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

## Installation
Objconf can be installed using pip:
```bash
python3 -m pip install objconf 
```

## Documentation
### Quickstart
TODO
### Config
`Config` class is a base class for your configuration class.
```python
from obj
```
### Attributes



## Tests
Objconf uses tox to run the tests.
```bash
python3 -m pip install tox
python3 -m tox
```
