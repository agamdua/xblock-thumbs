from unittest import TestCase
from thumbs import ThumbsBlock
from xblock.runtime import Runtime
from mock import MagicMock
import json


class TestThumbs(TestCase):

    def setUp(self):
        self.runtime = Runtime()
        self.thumbs = ThumbsBlock(self.runtime, {})

    def test_invalid_vote(self):
        self.data = MagicMock()
        self.data.body = json.dumps({'vote_type': 'top'})
        self.assertIsNone(json.loads(self.thumbs.vote(self.data).body))

    def test_up_vote(self):
        self.data = MagicMock()
        self.data.body = json.dumps({'vote_type': 'up'})
        self.assertEquals(json.loads(self.thumbs.vote(self.data).body), {'up': 1, 'down': 0})

    def test_down_vote(self):
        self.data = MagicMock()
        self.data.body = json.dumps({'vote_type': 'down'})
        self.assertEquals(json.loads(self.thumbs.vote(self.data).body), {'up': 0, 'down': 1})

    def test_multiple_votes(self):
        self.up = MagicMock()
        self.down = MagicMock()
        self.invalid = MagicMock()
        self.up.body = json.dumps({'vote_type': 'up'})
        self.down.body = json.dumps({'vote_type': 'down'})
        self.invalid.body = json.dumps({'vote_type': 'strange'})
        self.thumbs.vote(self.up)
        self.thumbs.vote(self.up)
        self.thumbs.vote(self.down)
        self.thumbs.vote(self.down)
        self.thumbs.vote(self.down)
        self.assertEquals(self.thumbs.upvotes, 2)
        self.assertEquals(self.thumbs.downvotes, 3)
