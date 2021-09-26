import io
import os
import pytest
import json
import yaml

from objconf import Config
from objconf import Attribute

TESTING_DATA_DIR = 'assets'


def data_path_join(file: str, data_dir: str = TESTING_DATA_DIR) -> str:
    return os.path.join(os.path.dirname(os.path.realpath(__file__)), data_dir, file)


@pytest.fixture
def config_yaml():
    with open(data_path_join('test-config.yaml')) as f:
        return io.StringIO(f.read())


@pytest.fixture
def config_json(config_yaml):
    return io.StringIO(json.dumps(yaml.safe_load(config_yaml)))


@pytest.fixture
def config_ini():
    with open(data_path_join('test-config.ini')) as f:
        return io.StringIO(f.read())


@pytest.fixture
def TestConfig():
    class TestConfiguration(Config):
        string_attr = Attribute(str)
        string_attr_default = Attribute(str, default='Default string')

        int_attr_key = Attribute(int, key='int_attr')

        list_attr = Attribute(list)

        bool_attr = Attribute(bool)

        def assert_config(self, ini=False):
            assert self.string_attr == 'string_attribute value'
            assert self.string_attr_default == self.__class__.string_attr_default.default
            assert self.int_attr_key == 12345
            assert self.bool_attr is True
            if not ini:
                assert self.list_attr == list(range(1, 6))

    return TestConfiguration
