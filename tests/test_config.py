import pytest


class TestYaml:
    def test_from_yaml(self, config_yaml, TestConfig):
        config = TestConfig.from_yaml(config_yaml)
        config.assert_config()


class TestJson:
    def test_from_yaml(self, config_json, TestConfig):
        config = TestConfig.from_yaml(config_json)
        config.assert_config()


class TestConfig:
    def test_independence_of_multiple_instances(self, config_yaml, TestConfig):
        one = TestConfig.from_yaml(config_yaml)
        config_yaml.seek(0)
        two = TestConfig.from_yaml(config_yaml)
        one.int_attr_key += 1
        assert one.int_attr_key == two.int_attr_key + 1

    def test_validator_success(self, config_yaml, TestConfig):
        TestConfig.bool_attr.validator = lambda x: x
        config = TestConfig.from_yaml(config_yaml)
        config.assert_config()

    def test_validator_fail(self, config_yaml, TestConfig):
        TestConfig.bool_attr.validator = lambda x: False
        with pytest.raises(ValueError):
            TestConfig.from_yaml(config_yaml)
