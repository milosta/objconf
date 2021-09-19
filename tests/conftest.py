import io
import os
import pytest
import json
import yaml

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
