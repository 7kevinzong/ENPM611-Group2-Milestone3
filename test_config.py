import unittest
import os
import json
import tempfile
from unittest import mock

import config

class TestConfig(unittest.TestCase):
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

    def test_get_parameter_missing_with_default(self):
        with mock.patch('os.getcwd', return_value='/nonexistent'):
            config._config = None
            self.assertEqual(config.get_parameter('NON_EXISTENT', default='default_value'), 'default_value')

    def test_get_parameter_missing_no_default(self):
        with mock.patch('os.getcwd', return_value='/nonexistent'):
            config._config = None
            self.assertIsNone(config.get_parameter('NON_EXISTENT'))

    def test_convert_to_typed_value_valid_json(self):
        self.assertEqual(config.convert_to_typed_value('{"a": 1}'), {"a": 1})

    def test_convert_to_typed_value_invalid_json(self):
        self.assertEqual(config.convert_to_typed_value('invalid'), 'invalid')

    def test_set_parameter_string(self):
        config.set_parameter('NEW_PARAM', 'test_value')
        self.assertEqual(os.environ['NEW_PARAM'], 'test_value')

    def test_set_parameter_json(self):
        config.set_parameter('NEW_PARAM', {"a": 1})
        self.assertTrue(os.environ['NEW_PARAM'].startswith('json:'))
        self.assertEqual(json.loads(os.environ['NEW_PARAM'][5:]), {"a": 1})

if __name__ == '__main__':
    unittest.main()
