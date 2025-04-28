import unittest
from unittest.mock import patch, MagicMock
from example_analysis import ExampleAnalysis

class TestExampleAnalysis(unittest.TestCase):

    @patch("example_analysis.config.get_parameter")
    @patch("example_analysis.DataLoader")
    @patch("example_analysis.plt.show")
    def test_run_without_user(self, mock_show, mock_dataloader, mock_get_parameter):
        mock_get_parameter.return_value = None

        mock_issue = MagicMock(
            creator = "creator1",
            events = [
                MagicMock(author="user1"),
                MagicMock(author="user2")
            ]
        )

        mock_dataloader.return_value.get_issues.return_value = [mock_issue]

        analysis = ExampleAnalysis()
        analysis.run()

        mock_get_parameter.assert_called_with('user')
        mock_dataloader.return_value.get_issues.assert_called_once()
        mock_show.assert_called_once()

    @patch("example_analysis.config.get_parameter")
    @patch("example_analysis.DataLoader")
    @patch("example_analysis.plt.show")
    def test_run_with_user_filter(self, mock_show, mock_dataloader, mock_get_parameter):
        mock_get_parameter.return_value = "user1"

        mock_issue = MagicMock(
            creator = "creator1",
            events = [
                MagicMock(author="user1"),
                MagicMock(author="user2")
            ]
        )

        mock_dataloader.return_value.get_issues.return_value = [mock_issue]

        analysis = ExampleAnalysis()
        analysis.run()

        mock_get_parameter.assert_called_with('user')
        mock_dataloader.return_value.get_issues.assert_called_once()
        mock_show.assert_called_once()

if __name__ == "__main__":
    unittest.main()