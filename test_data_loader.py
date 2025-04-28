import unittest
import tempfile
import os

from unittest.mock import patch, mock_open
import json
from data_loader import DataLoader, _ISSUES

# michael additions
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

# remote 
class TestDataLoader(unittest.TestCase):
    def test_invalid_dataset_selection(self):
        with self.assertRaises(ValueError):
            DataLoader(2)

        with self.assertRaises(ValueError):
            DataLoader(-1)

    @patch("data_loader.config.get_parameter")
    def test_valid_dataset_selection(self, mock_get_parameter):
        mock_get_parameter.side_effect = lambda key: "./partial.json" if key == "ENPM611_PROJECT_DATA_PATH" else "./all.json"

        self.assertEqual(DataLoader().data_path, "./partial.json")
        self.assertEqual(DataLoader(0).data_path, "./partial.json")
        self.assertEqual(DataLoader(1).data_path, "./all.json")

    @patch("data_loader.Issue")
    @patch("builtins.open", new_callable=mock_open, read_data=json.dumps([
        {"id": 1, "title": "Issue 1"},
        {"id": 2, "title": "Issue 2"}
    ]))
    @patch("data_loader.config.get_parameter", return_value="./all.json")
    def test_get_issues(self, mock_get_parameter, mock_open, mock_issue):
        loader = DataLoader()
        issues = loader.get_issues()

        mock_open.assert_called_once_with("./all.json", "r")

        self.assertEqual(mock_issue.call_count, 2)
        self.assertEqual(len(issues), 2)

        # Check the returned issues are from the Issue constructor
        self.assertEqual(issues[0], mock_issue.return_value)
        self.assertEqual(issues[1], mock_issue.return_value)

        # Check that get_issues caches results and doesn't call open again
        second_call = loader.get_issues()
        self.assertIs(issues, second_call)
        mock_open.assert_called_once()

if __name__ == '__main__':
    unittest.main()