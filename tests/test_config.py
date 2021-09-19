from objconf.config import Config
from objconf.attributes import Attribute


class TestConfig(Config):
    string_attr = Attribute(str)
    string_attr_default = Attribute(str, default='Default string')

    int_attr_key = Attribute(int, key='int_attr')

    list_attr = Attribute(list)

    bool_attr = Attribute(bool, validator=lambda x: x)  # Validate val is true

    def assert_config(self):
        assert self.string_attr == 'string_attribute value'
        assert self.string_attr_default == self.__class__.string_attr_default.default
        assert self.int_attr_key == 12345
        assert self.list_attr == list(range(1, 6))
        assert self.bool_attr is True


class TestYaml(TestConfig):
    def test_from_yaml(self, config_yaml):
        config = self.from_yaml(config_yaml)
        config.assert_config()


class TestJson(TestConfig):
    def test_from_yaml(self, config_json):
        config = self.from_yaml(config_json)
        config.assert_config()

# TODO: test transformer
