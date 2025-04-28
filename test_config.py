import unittest
import os
import json
from unittest.mock import patch, mock_open, Mock, MagicMock
import config


class TestConfig(unittest.TestCase):

    def setUp(self):
        config._config = None  # Reset before each test

    @patch.dict(os.environ, {"TEST_PARAM": "simple_value"})
    def test_get_parameter_from_env(self):
        result = config.get_parameter("TEST_PARAM")
        self.assertEqual(result, "simple_value")

    @patch.dict(os.environ, {"COMPLEX_PARAM": 'json:{"key": "val"}'})
    def test_get_json_parameter_from_env(self):
        value = config.get_parameter("COMPLEX_PARAM")
        self.assertEqual(value, {"key": "val"})

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

if __name__ == "__main__":
    unittest.main()
