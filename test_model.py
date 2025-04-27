import unittest
from datetime import datetime
from model import Event, Issue, State

class TestEvent(unittest.TestCase):
    def test_event_from_valid_json(self):
        jobj = {
            'event_type': 'labeled',
            'author': 'bob',
            'event_date': '2024-04-25T00:00:00Z',
            'label': 'kind/bug',
            'comment': 'fix this'
        }
        event = Event(jobj)
        self.assertEqual(event.event_type, 'labeled')
        self.assertEqual(event.author, 'bob')
        self.assertIsInstance(event.event_date, datetime)
        self.assertEqual(event.label, 'kind/bug')
        self.assertEqual(event.comment, 'fix this')

    def test_event_from_invalid_date(self):
        jobj = {
            'event_type': 'labeled',
            'author': 'bob',
            'event_date': 'blahblahblah',
            'label': 'king/bug',
            'comment': 'fix me'
        }
        event = Event(jobj)
        self.assertIsNone(event.event_date)

    def test_event_from_none(self):
        event = Event(None)
        self.assertIsNone(event.event_type)
        self.assertIsNone(event.author)
        self.assertIsNone(event.event_date)
        self.assertIsNone(event.label)
        self.assertIsNone(event.comment)


class TestIssue(unittest.TestCase):
    def test_issue_from_valid_json(self):
        jobj = {
            'url': 'http://github.com/issue/1',
            'creator': 'kevin',
            'labels': ['kind/bug', 'status/triage'],
            'state': 'open',
            'assignees': ['bob', 'kevin'],
            'title': 'Fix this',
            'text': 'This needs to be fixed',
            'number': 10,
            'created_date': '2024-04-25T00:00:00Z',
            'updated_date': '2024-04-25T01:00:00Z',
            'timeline_url': 'http://github.com/issue/1/timeline',
            'events': [
                {
                    'event_type': 'commented',
                    'author': 'bob',
                    'event_date': '2024-04-25T01:00:00Z',
                    'comment': 'Looking into this'
                }
            ]
        }
        issue = Issue(jobj)
        self.assertEqual(issue.url, 'http://github.com/issue/1')
        self.assertEqual(issue.creator, 'kevin')
        self.assertEqual(issue.labels, ['kind/bug', 'status/triage'])
        self.assertEqual(issue.state, State.open)
        self.assertEqual(issue.assignees, ['bob', 'kevin'])
        self.assertEqual(issue.title, 'Fix this')
        self.assertEqual(issue.text, 'This needs to be fixed')
        self.assertEqual(issue.number, 10)
        self.assertIsInstance(issue.created_date, datetime)
        self.assertIsInstance(issue.updated_date, datetime)
        self.assertEqual(issue.timeline_url, 'http://github.com/issue/1/timeline')
        self.assertEqual(len(issue.events), 1)
        self.assertIsInstance(issue.events[0], Event)

    def test_issue_invalid_number(self):
        jobj = {
            'state': 'closed',
            'number': 'invalid_number'
        }
        issue = Issue(jobj)
        self.assertEqual(issue.number, -1)
        self.assertEqual(issue.state, State.closed)

    def test_issue_invalid_dates(self):
        jobj = {
            'state': 'open',
            'created_date': 'some_date',
            'updated_date': 'other_date'
        }
        issue = Issue(jobj)
        self.assertIsNone(issue.created_date)
        self.assertIsNone(issue.updated_date)

    def test_issue_from_none(self):
        issue = Issue(None)
        self.assertIsNone(issue.url)
        self.assertEqual(issue.labels, [])
        self.assertEqual(issue.assignees, [])
        self.assertEqual(issue.number, -1)
        self.assertEqual(issue.events, [])

if __name__ == '__main__':
    unittest.main()