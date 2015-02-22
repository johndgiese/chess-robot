import chess as c
import util as u

def test_adjacent_squares():
    assert sorted(list(u.adjacent_squares(c.A1))) == sorted([c.B1, c.B2, c.A2])
    assert sorted(list(u.adjacent_squares(c.A2))) == sorted([c.A1, c.B1, c.B2, c.A3, c.B3])
    assert sorted(list(u.adjacent_squares(c.B2))) == sorted([c.A1, c.B1, c.C1, c.A2, c.C2, c.A3, c.B3, c.C3])

    assert sorted(list(u.adjacent_squares(c.H8))) == sorted([c.G7, c.H7, c.G8])
    assert sorted(list(u.adjacent_squares(c.A8))) == sorted([c.A7, c.B7, c.B8])
