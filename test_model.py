import unittest
from model import State, Event, Issue

class TestModel(unittest.TestCase):
    def setUp(self):
        self.state = State()
        self.event = Event()
        self.issue = Issue()

    def test_state_from_json(self):

    def test_event_from_json(self):

    def test_issue_from_json(self):


if __name__ == "__main__":
    unittest.main()