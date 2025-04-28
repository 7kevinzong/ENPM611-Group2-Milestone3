import unittest
from unittest.mock import patch, MagicMock

from analysis_2 import Analysis2

class TestAnalysis2(unittest.TestCase):

    # test reading dataset ID
    @patch("analysis_2.config.get_parameter")
    def test_init_sets_dataset(self, mock_get_parameter):
        mock_get_parameter.return_value = 1

        analysis = Analysis2()
        self.assertEqual(analysis.DATASET, 1)

    # test if config.get_parameter is not called, DATASET defaults to 0 
    def test_init_sets_default_dataset_when_none(self):
        analysis = Analysis2()
        self.assertEqual(analysis.DATASET, 0)

    # test creating and showing graph
    @patch("analysis_2.go.Figure.show")
    @patch("analysis_2.DataLoader.get_issues")
    def test_run_creates_graph_and_shows_figure(self, mock_get_issues, mock_show):
        mock_issue = MagicMock(
            creator = "user1",
            events = [
                MagicMock(author="user2"),
                MagicMock(author="user1"),
                MagicMock(author=None)
            ]
        )

        mock_get_issues.return_value = [mock_issue]

        analysis = Analysis2()
        analysis.run()

        expected_nodes = {"user1", "user2"}
        self.assertSetEqual(set(analysis.nxG.nodes), expected_nodes)

        self.assertTrue(analysis.nxG.has_edge("user1", "user2"))
        self.assertEqual(analysis.nxG["user1"]["user2"]["weight"], 1)

        mock_show.assert_called_once()

    # test empty issue handling
    @patch("analysis_2.go.Figure")
    @patch("analysis_2.DataLoader.get_issues")
    def test_no_issues_empty_graph(self, mock_get_issues, mock_fig):
        mock_get_issues.return_value = []

        analysis = Analysis2()
        analysis.run()

        self.assertEqual(len(analysis.nxG.nodes()), 0)
        self.assertEqual(len(analysis.nxG.edges()), 0)
        mock_fig.return_value.show.assert_called_once()

if __name__ == "__main__":
    unittest.main()