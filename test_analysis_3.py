import unittest
from unittest.mock import patch
from analysis_3 import Analysis3
from model import Issue, State

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

        mock_plt_show.assert_not_called()

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