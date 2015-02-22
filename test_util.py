import chess as c
import util as u

def test_adjacent_squares():
    assert sorted(list(u.adjacent_squares(c.A1))) == sorted([c.B1, c.B2, c.A2])
    assert sorted(list(u.adjacent_squares(c.A2))) == sorted([c.A1, c.B1, c.B2, c.A3, c.B3])
    assert sorted(list(u.adjacent_squares(c.B2))) == sorted([c.A1, c.B1, c.C1, c.A2, c.C2, c.A3, c.B3, c.C3])

    assert sorted(list(u.adjacent_squares(c.H8))) == sorted([c.G7, c.H7, c.G8])
    assert sorted(list(u.adjacent_squares(c.A8))) == sorted([c.A7, c.B7, c.B8])

def test_pawn_protecting_squares():
    assert sorted(u.pawn_protecting_squares(c.WHITE, c.B6)) == sorted([c.A5, c.C5])
    assert sorted(u.pawn_protecting_squares(c.BLACK, c.B6)) == sorted([c.A7, c.C7])
    assert sorted(u.pawn_protecting_squares(c.WHITE, c.A6)) == sorted([c.B5])
    assert sorted(u.pawn_protecting_squares(c.BLACK, c.A6)) == sorted([c.B7])
