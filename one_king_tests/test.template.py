import chess

from unittest import TestCase
from util import num_kings


class TestGame(TestCase):
    def setUp(self):
        b = chess.Bitboard()
        {% for m in moves %}
        b.push(chess.Move({{ m.from_square }}, {{ m.to_square }}, {{ m.promotion }}) # {{ m }}
        {% endfor %}
        self.board = b


    def test_kings(self):
        self.assertEqual(num_kings(self.board), 2)

