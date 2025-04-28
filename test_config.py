import unittest
import os
import json
import tempfile
from unittest import mock
from unittest.mock import patch, mock_open, Mock, MagicMock

import config

class TestConfig(unittest.TestCase):
    def setUp(self):
        config._config = None  # Reset before each test

    def test_get_parameter_from_env(self):
        os.environ['TEST_PARAM'] = 'test_value'
        self.assertEqual(config.get_parameter('TEST_PARAM'), 'test_value')

    def test_get_parameter_from_env_json(self):
        os.environ['TEST_PARAM'] = 'json:{"key": "value"}'
        self.assertEqual(config.get_parameter('TEST_PARAM'), {"key": "value"})

    def test_get_parameter_from_config_file(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            filepath = os.path.join(tmpdir, 'config.json')
            with open(filepath, 'w') as f:
                json.dump({"PARAM": "file_value"}, f)

            with mock.patch('os.getcwd', return_value=tmpdir):
                config._config = None
                self.assertEqual(config.get_parameter('PARAM'), 'file_value')

    def test_convert_to_typed_value_valid_json(self):
        self.assertEqual(config.convert_to_typed_value('{"a": 1}'), {"a": 1})

    def test_convert_to_typed_value_invalid_json(self):
        self.assertEqual(config.convert_to_typed_value('invalid'), 'invalid')

    @patch.dict(os.environ, {}, clear=True)
    def test_get_parameter_returns_default(self):
        fallback = config.get_parameter("MISSING", default="backup_value")
        self.assertEqual(fallback, "backup_value")

    @patch.dict(os.environ, {}, clear=True)
    def test_get_parameter_none_if_missing(self):
        self.assertIsNone(config.get_parameter("NOT_DEFINED"))

    @patch("config.os.getcwd", return_value="/nonexistent")
    @patch("config.os.path.isfile", return_value=False)
    def test_get_default_path_not_found(self, mock_isfile, mock_getcwd):
        path = config._get_default_path()
        self.assertIsNone(path)

    @patch("config._get_default_path", return_value=None)
    def test_init_config_sets_empty_when_no_file(self, mock_path):
        config._init_config()
        self.assertEqual(config._config, {})

    @patch("builtins.open", new_callable=mock_open, read_data=json.dumps({"key": "value"}))
    @patch("config._get_default_path", return_value="dummy.json")
    def test_init_config_loads_file(self, mock_path, mock_file):
        config._init_config()
        self.assertEqual(config._config, {"key": "value"})

    @patch.dict(os.environ, {}, clear=True)
    def test_set_parameter_stores_string(self):
        config.set_parameter("NEW_KEY", "hello")
        self.assertEqual(os.environ["NEW_KEY"], "hello")

    @patch.dict(os.environ, {}, clear=True)
    def test_set_parameter_stores_json(self):
        obj = {"a": 1}
        config.set_parameter("OBJ_KEY", obj)
        self.assertTrue(os.environ["OBJ_KEY"].startswith("json:"))
        parsed = json.loads(os.environ["OBJ_KEY"][5:])
        self.assertEqual(parsed, obj)

    @patch("config._get_default_path")
    @patch("builtins.open", create=True)
    def test_init_config_handles_invalid_json(self, mock_open, mock_get_path):
        mock_get_path.return_value = "./invalid.json"
        mock_open.return_value.__enter__.return_value.read.return_value = "invalid json"

        try:
            config._init_config()
        except Exception as e:
            self.fail(f"_init_config() raised an exception on invalid JSON: {e}")

if __name__ == "__main__":
    unittest.main()
