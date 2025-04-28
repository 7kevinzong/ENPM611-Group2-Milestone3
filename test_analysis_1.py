import unittest
from unittest.mock import patch, MagicMock
from analysis_1 import Analysis1
from datetime import datetime

class TestAnalysis1(unittest.TestCase):
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

        analysis = Analysis1()
        analysis.run()

        mock_show.assert_called_once()

    @patch("analysis_1.DataLoader")
    def test_run_handles_none_issues(self, mock_dataloader):
        mock_dataloader.return_value.get_issues.return_value = None

        analysis = Analysis1()

        try:
            analysis.run()
        except Exception as e:
            self.fail(f"run() raised an exception when issues=None: {e}")

if __name__ == "__main__":
    unittest.main()