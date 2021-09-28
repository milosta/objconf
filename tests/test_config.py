import io
import pytest

from objconf import Attribute
from objconf import Config


class TestYaml:
    def test_from_yaml(self, config_yaml, TestConfig):
        config = TestConfig.load_yaml(config_yaml)
        config.assert_config()


class TestJson:
    def test_from_yaml(self, config_json, TestConfig):
        config = TestConfig.load_yaml(config_json)
        config.assert_config()


class TestIni:
    def test_from_ini_one_section(self, config_ini, TestConfig):
        del TestConfig.list_attr

        config = TestConfig.load_ini(config_ini, ['default'])
        config.assert_config(ini=True)

    def test_from_ini_all_sections(self, config_ini, TestConfig):
        del TestConfig.list_attr
        TestConfig.second_str = Attribute(str)
        TestConfig.second_str.__set_name__(TestConfig, 'second_str')

        config = TestConfig.load_ini(config_ini)
        config.assert_config(ini=True)

    def test_from_ini_interpolation(self):
        config_ini = io.StringIO('[default]\n'
                                 'string_attr=string_attr\n'
                                 'interpolation=%(string_attr)s\n')

        class InterpolationConfig(Config):
            string_attr = Attribute(str)
            interpolation = Attribute(str)

        config = InterpolationConfig.load_ini(config_ini)
        assert config.string_attr == config.interpolation


class TestConfig:
    def test_independence_of_multiple_instances(self, config_yaml, TestConfig):
        one = TestConfig.load_yaml(config_yaml)
        config_yaml.seek(0)
        two = TestConfig.load_yaml(config_yaml)
        one.int_attr_key += 1
        assert one.int_attr_key == two.int_attr_key + 1

    def test_validator_success(self, config_yaml, TestConfig):
        TestConfig.bool_attr.validator = lambda x: x
        config = TestConfig.load_yaml(config_yaml)
        config.assert_config()

    def test_validator_fail(self, config_yaml, TestConfig):
        TestConfig.bool_attr.validator = lambda x: False
        with pytest.raises(ValueError):
            TestConfig.load_yaml(config_yaml)

    def test_transformer(self, config_yaml, TestConfig):
        transformed = 'transformed'
        TestConfig.string_attr.transformer = lambda x: transformed
        TestConfig.string_attr.validator = lambda x: x == transformed
        config = TestConfig.load_yaml(config_yaml)
        assert config.string_attr == transformed


class TestDocumentationExamples:
    def test_config_example(self):
        # Define configuration
        class AppConfig(Config):
            simple_string_attr = Attribute(str)
            int_attr_with_default = Attribute(int, default=5)
            bool_attr_different_key = Attribute(bool, key='actual_bool_key')
            int_over_ten = Attribute(int, validator=lambda x: x > 10)
            upper_str_attr = Attribute(str, transformer=str.upper)

        # Load configuration
        yaml_config = '''
        simple_string_attr: string_value
        actual_bool_key: True
        int_over_ten: 42
        upper_str_attr: lower
        '''
        app_config = AppConfig.load_yaml(io.StringIO(yaml_config))

        assert app_config.int_attr_with_default == 5
        assert app_config.upper_str_attr == 'LOWER'
