import chess as c
import weight as w


def test_pawn_structure_weight():

    # black has two "pawn protections"
    b = c.Bitboard('rnbqkbnr/ppp1pppp/3p4/8/3P4/8/PPP1PPPP/RNBQKBNR w KQkq - 0 2')
    assert w.pawn_structure_weight(b) == -1/2

    # black has doubled pawn
    b = c.Bitboard('rnbqkbnr/pp2pppp/8/3p4/3p4/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1')
    assert w.pawn_structure_weight(b) == 1/2

    # black has three doubled pawns
    b = c.Bitboard('rnbqkbnr/ppp5/6p1/3p2p1/3p2p1/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1')
    assert w.pawn_structure_weight(b) == 3*4/8

    b = c.Bitboard('rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1')
    assert w.pawn_structure_weight(b) == 0

    b = c.Bitboard('rnbqkbnr/pppppppp/8/8/8/P7/1PPPPPPP/RNBQKBNR w KQkq - 0 1')
    assert w.pawn_structure_weight(b) == 1*2/8

    b = c.Bitboard('rnbqkbnr/pppppppp/8/8/8/3P4/PPP1PPPP/RNBQKBNR w KQkq - 0 1')
    assert w.pawn_structure_weight(b) == 1/2

    b = c.Bitboard('rnbqkbnr/pppppppp/8/8/3P4/8/PPP1PPPP/RNBQKBNR w KQkq - 0 1')
    assert w.pawn_structure_weight(b) == 0

    # black has elaborate connected pawn chain with 1 pawn missing
    b = c.Bitboard('rnbqkbnr/p5p1/1p3p2/2p1p3/3p4/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1')
    assert w.pawn_structure_weight(b) == -(6*2)/7

