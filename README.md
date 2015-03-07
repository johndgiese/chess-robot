![Example Moves](https://raw.github.com/johndgiese/chess-robot/master/chess.png)

# Chess Robot

Two good friends of mine were visiting for the weekend.  We wanted to build something fun together on one of the days, so after some deliberation, we decided to build a simple chess AI.  Of course this problem has been solved 100's of times, so it is not novel in anyway, but it was a fun chance to work with some interesting algorithms and build something small and fun.

# Outline

We divided the work into a few functions:

1. Given a board state, return who is more likely to win (positive numbers mean player 1, negative mean player 2).
2. Given a board state, return all possible moves that can be made.
3. Given a board state and a move, return a new board state.
4. Given a board, return the optimal move.

The first function (the board state evaluator) is a simple function that usually it involves a number of heuristics about the game.  Functions two and three are non-trivial but straightforward.  The last function is the hardest.

We used decision-making algorithm based on the [mini-max algorithm](http://en.wikipedia.org/wiki/Minimax)---this was the algorithm used in Deep Blue.

# Our Chess Board State Evaluator

For chess, our board state evaluator has a number of heuristics it uses to evaluation a position.  For example:

- Balance of pieces on the board
- How much you are attacking the other persons King
- Your control of the center
- Your pawn structure
- The safety of your King

# Our Connect Four State Evaluator

Haven't finisehd building this yet!

# Simple Optimizations

The board state evaluator is called many many times (in the millions over the course of a game, even when only looking three moves in the future).  Often times on the same board position (e.g. if you consider permutations of a different series of independent moves).  To optimize for this, we used an LRU cache.  We could simply memoize the results, however, this would require substantial memory overhead, and after a few moves, the previous board states may become unlikely or impossible.  After while, we switched to an sqlite database for caching so it would work between game runs.

Some optimization was also done in the move-selector algorithm itself, to throw away bad paths before traversing them fully.


# Setup

Create a virtualenv for python3.  Install python requirements from "requirements.txt".  Run the "db_cache.py" function as a script, then run "play_chess.py".

For example:

```
virtualenv -p python3 env
source env/bin/activate
pip install -r requirements.txt
python db_cache.py
python play_chess.py
```

