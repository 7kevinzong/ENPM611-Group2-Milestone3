import unittest
import tempfile
import json
import os

from unittest.mock import patch

import data_loader
from data_loader import DataLoader, Issue

class TestDataLoader(unittest.TestCase):
    def setUp(self):
        data_loader._ISSUES = None

    # test for invalid dataset
    def test_invalid_dataset_selection(self):
        with self.assertRaises(ValueError):
            DataLoader(dataset=2)

    # test for if JSON file is empty it returns an empty list
    def test_get_issues_empty_json(self):

        with tempfile.NamedTemporaryFile('w+', delete=False) as tf:
            tf.write("[]")
            tf.flush()
            path = tf.name

        with patch('data_loader.config.get_parameter', return_value=path), \
             patch('data_loader.Issue', side_effect=lambda x: x):
            loader = DataLoader()
            issues = loader.get_issues()
            self.assertEqual(issues, [])

        os.remove(path)

    # test for error handling if data is malformed
    def test_load_malformed_json_raises(self):

        with tempfile.NamedTemporaryFile('w+', delete=False) as tf:
            tf.write("{ not valid json ]")
            tf.flush()
            path = tf.name

        with patch('data_loader.config.get_parameter', return_value=path):
            loader = DataLoader()

            with self.assertRaises(json.JSONDecodeError):
                loader.get_issues()

        os.remove(path)

if __name__ == '__main__':
    unittest.main()