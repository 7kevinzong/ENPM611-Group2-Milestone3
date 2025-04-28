import unittest
from unittest.mock import patch, MagicMock
from analysis_3 import Analysis3
from model import Issue, Event, State
from datetime import datetime
from io import StringIO

class TestAnalysis3(unittest.TestCase):
    @patch("analysis_3.plt.show")
    @patch("analysis_3.DataLoader")
    @patch("analysis_3.config.get_parameter")
    def test_no_closed_issues(self, mock_get_parameter, mock_dataloader, mock_plt_show):
        mock_get_parameter.side_effect = lambda key: None
        mock_dataloader.return_value.get_issues.return_value = [
            Issue(
                {
                    "number": 1,
                    "title": "Open Issue",
                    "state": State.open,
                    "labels": [],
                    "events": [],
                    "creator": "user1",
                    "created_date": "2023-01-01T00:00:00Z",
                    "updated_date": "2023-01-03T00:00:00Z"
                }
            )
        ]

        analysis = Analysis3()
        analysis.run()

    @patch("analysis_3.config.get_parameter")
    def test_dataset_initialization(self, mock_get_parameter):
        # Simulate a scenario where the dataset is not set in the config
        mock_get_parameter.side_effect = lambda key: None if key == "dataset" else None

        analysis = Analysis3()

        # Ensure that self.DATASET is set to 0 by default
        self.assertEqual(analysis.DATASET, 0)

    @patch("matplotlib.pyplot.show")
    @patch("analysis_3.DataLoader")
    @patch("analysis_3.config.get_parameter")
    @patch("sys.stdout", new_callable=StringIO)
    def test_run_with_closed_issues(self, mock_stdout, mock_get_parameter, mock_dataloader, mock_show):
        mock_get_parameter.side_effect = lambda key: "bug" if key == "label" else 0

        fake_issue_data = {
            "number": 1,
            "title": "Fake Issue",
            "creator": "user1",
            "labels": ["bug"],
            "created_date": "2023-01-01T00:00:00Z",
            "updated_date": "2023-01-05T00:00:00Z",
            "state": "closed",
            "events": [
                {
                    "event_type": "comment",
                    "author": "user1",
                    "event_date": "2023-01-02T00:00:00Z",
                    "comment": "sample comment",
                }
            ],
        }

        mock_dataloader.return_value.get_issues.return_value = [Issue(fake_issue_data)]
        analysis = Analysis3()
        analysis.run()

        output = mock_stdout.getvalue()
        self.assertIn("Analyzing 1 closed issues with label bug", output)



    @patch("matplotlib.pyplot.show")
    @patch("analysis_3.DataLoader")
    @patch("analysis_3.config.get_parameter")
    @patch("sys.stdout", new_callable=StringIO)
    def test_run_with_no_closed_issues(self,mock_stdout , mock_get_parameter, mock_dataloader, mock_show):
        mock_get_parameter.side_effect = lambda key: "bug" if key == "label" else 0

        fake_issue_data = {
            "number": 1,
            "title": "Fake Issue",
            "creator": "user1",
            "labels": ["bug"],
            "created_date": "2023-01-01T00:00:00Z",
            "updated_date": "2023-01-05T00:00:00Z",
            "state": "open",
            "events": [
                {
                    "event_type": "comment",
                    "author": "user1",
                    "event_date": "2023-01-02T00:00:00Z",
                    "comment": "sample comment",
                }
            ],
        }

        mock_dataloader.return_value.get_issues.return_value = [Issue(fake_issue_data)]
        analysis = Analysis3()
        analysis.run()
        output = mock_stdout.getvalue()
        self.assertIn("No closed issues found in the dataset.", output)


    @patch("matplotlib.pyplot.show")
    @patch("analysis_3.DataLoader")
    @patch("analysis_3.config.get_parameter")
    @patch("sys.stdout", new_callable=StringIO)
    def test_run_with_label_mismatch(self, mock_stdout, mock_get_parameter, mock_dataloader, mock_show):
        mock_get_parameter.side_effect = lambda key: "security" if key == "label" else 0

        issue_data = {
            "number": 2,
            "title": "Label mismatch test",
            "creator": "user2",
            "labels": ["bug"],
            "created_date": "2023-03-01T00:00:00Z",
            "updated_date": "2023-03-05T00:00:00Z",
            "state": "closed",
            "events": [],
        }

        mock_dataloader.return_value.get_issues.return_value = [Issue(issue_data)]
        analysis = Analysis3()
        analysis.run()
        output = mock_stdout.getvalue()
        self.assertIn("Analyzing 0 closed issues with label security", output)

    @patch("matplotlib.pyplot.show")
    @patch("analysis_3.DataLoader")
    @patch("analysis_3.config.get_parameter")
    @patch("sys.stdout", new_callable=StringIO)
    def test_issue_with_different_comment_author(self,mock_stdout,  mock_get_parameter, mock_dataloader, mock_show):
        mock_get_parameter.side_effect = lambda key: "bug" if key == "label" else 0

        issue_data = {
            "number": 3,
            "title": "Author mismatch",
            "creator": "user3",
            "labels": ["bug"],
            "created_date": "2023-04-01T00:00:00Z",
            "updated_date": "2023-04-03T00:00:00Z",
            "state": "closed",
            "events": [
                {
                    "event_type": "comment",
                    "author": "other_user",
                    "event_date": "2023-04-02T00:00:00Z",
                    "comment": "Helpful comment",
                }
            ],
        }

        mock_dataloader.return_value.get_issues.return_value = [Issue(issue_data)]
        analysis = Analysis3()
        analysis.run()
        output = mock_stdout.getvalue()
        self.assertIn("Fastest resolution time: 2 days\nSlowest resolution time: 2 days", output)

    @patch("matplotlib.pyplot.show")
    @patch("analysis_3.DataLoader")
    @patch("analysis_3.config.get_parameter")
    @patch("sys.stdout", new_callable=StringIO)
    def test_run_with_invalid_data(self,mock_stdout, mock_get_parameter, mock_dataloader, mock_show):
        # Test invalid data in the issue
        mock_get_parameter.side_effect = lambda key: "bug" if key == "label" else 0

        invalid_issue_data = {
            "number": 1,
            "title": "Invalid Issue",
            "creator": "user4",
            "labels": ["bug"],
            "created_date": "invalid_date",
            "updated_date": "invalid_date",
            "state": "closed",
            "events": [],
        }

        mock_dataloader.return_value.get_issues.return_value = [Issue(invalid_issue_data)]
        analysis = Analysis3()

        analysis.run()

        output = mock_stdout.getvalue()
        self.assertIn("No valid lifecycle data found to analyze.", output)

        mock_show.assert_not_called()

    @patch("analysis_3.plt.show")
    @patch("analysis_3.DataLoader")
    @patch("analysis_3.config.get_parameter")
    def test_no_valid_lifecycle_data(self, mock_get_parameter, mock_dataloader, mock_plt_show):
        mock_get_parameter.side_effect = lambda key: None
        mock_dataloader.return_value.get_issues.return_value = [
            Issue(
                {
                    "number": 1,
                    "title": "Bad Dates",
                    "state": State.closed,
                    "labels": [],
                    "events": [],
                    "creator": "user1",
                    "created_date": None,
                    "updated_date": None
                }
            )
        ]

        analysis = Analysis3()
        analysis.run()

        mock_plt_show.assert_not_called()

    @patch("analysis_3.plt.show")
    @patch("analysis_3.DataLoader")
    @patch("analysis_3.config.get_parameter")
    def test_basic_resolution_analysis(self, mock_get_parameter, mock_dataloader, mock_plt_show):
        mock_get_parameter.side_effect = lambda key: None

        mock_dataloader.return_value.get_issues.return_value = [
            Issue(
                {
                    "number": 123,
                    "title": "Closed Issue",
                    "state": State.closed,
                    "labels": ["bug"],
                    "events": [
                        {
                            "author": "user2",
                            "comment": "fix this"
                        }
                    ],
                    "creator": "user1",
                    "created_date": "2023-01-01T00:00:00Z",
                    "updated_date": "2023-01-05T00:00:00Z"
                }
            )
        ]

        analysis = Analysis3()
        analysis.run()

        self.assertEqual(analysis.LABEL, None)
        mock_plt_show.assert_called()

    @patch("analysis_3.plt.show")
    @patch("analysis_3.DataLoader")
    @patch("analysis_3.config.get_parameter")
    def test_filter_by_label(self, mock_get_parameter, mock_dataloader, mock_plt_show):
        mock_get_parameter.side_effect = lambda key: "bug" if key == "label" else None

        mock_dataloader.return_value.get_issues.return_value = [
            Issue(
                {
                    "number": 1,
                    "title": "Bug Issue",
                    "state": State.closed,
                    "labels": ["bug"],
                    "events": [
                        {
                            "author": "user1",
                            "comment": "Looks good"
                        },
                        {
                            "author": "user2",
                            "comment": "Needs fix"
                        }
                    ],
                    "creator": "user1",
                    "created_date": "2023-01-01T00:00:00Z",
                    "updated_date": "2023-01-03T00:00:00Z"
                }
            ),
            Issue(
                {
                    "number": 2,
                    "title": "Feature Issue",
                    "state": State.closed,
                    "labels": ["feature"],
                    "events": [
                        {
                            "author": "user2",
                            "comment": "Implemented feature"
                        }
                    ],
                    "creator": "user2",
                    "created_date": "2023-01-01T00:00:00Z",
                    "updated_date": "2023-01-03T00:00:00Z"
                }
            )
        ]

        analysis = Analysis3()
        analysis.run()

        mock_plt_show.assert_called()

    @patch("analysis_3.plt.show")
    @patch("analysis_3.DataLoader")
    @patch("analysis_3.config.get_parameter")
    def test_negative_resolution_time_skipped(self, mock_get_parameter, mock_dataloader, mock_plt_show):
        mock_get_parameter.side_effect = lambda key: None
        mock_dataloader.return_value.get_issues.return_value = [
            Issue(
                {
                    "number": 10,
                    "title": "Bad Issue",
                    "state": State.closed,
                    "labels": ["bug"],
                    "events": [],
                    "creator": "user1",
                    "created_date": "2023-05-01T00:00:00Z",
                    "updated_date": "2023-04-30T00:00:00Z",
                }

            )
        ]

        analysis = Analysis3()
        analysis.run()

        mock_plt_show.assert_not_called()

if __name__ == "__main__":
    unittest.main()
