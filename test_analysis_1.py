import unittest
from unittest.mock import patch, MagicMock
from analysis_1 import Analysis1
from datetime import datetime

class TestAnalysis1(unittest.TestCase):
    def setUp(self):
        self.analysis1 = Analysis1()

    @patch("analysis_1.config.get_parameter")
    @patch("analysis_1.DataLoader")
    @patch("analysis_1.plt.show")
    def test_run_with_mocked_data(self, mock_show, mock_dataloader, mock_get_parameter):
        mock_get_parameter.side_effect = lambda key: "test_user" if key == "user" else 0

        mock_issues = [
            MagicMock(created_date=datetime(2023, 1, 15), creator="test_user"),
            MagicMock(created_date=datetime(2023, 2, 15), creator="test_user"),
            MagicMock(created_date=datetime(2023, 3, 15), creator="other_user"),
        ]

        mock_instance = mock_dataloader.return_value
        mock_instance.get_issues.return_value = mock_issues

        self.analysis1.run()

        mock_show.assert_called_once()

if __name__ == "__main__":
    unittest.main()