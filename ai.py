## Authors: Daniel Hensley and Ryan Orendorff
from functools import reduce

## Global definition of infinity.
inf = float('inf')

class Move(object):
    ''' A pair containing the action and its associated value.

    The important component of this class is that it can be compared, and
    hence passed to functions like min, max, etc.
    '''
    def __init__(self, action, value):
        self._action = action
        self._value = value

    @property
    def action(self):
        return self._action

    @property
    def value(self):
        return self._value

    def __eq__(self, other):
        return self.value == other.value

    def __ne__(self, other):
        return self.value != other.value

    def __lt__(self, other):
        return self.value < other.value

    def __le__(self, other):
        return self.value <= other.value

    def __gt__(self, other):
        return self.value > other.value

    def __ge__(self, other):
        return self.value >= other.value

    def __repr__(self):
        return "Move({}, {})".format(repr(self._action), self._value)

    ## For copy we are assuming action is immutable, and value is a number
    ## (which also makes it immutable).
    def copy(self):
        return Move(self._action, self._value)


def adversarial_search(value, actions, step, horizon=3):
    '''An AI function that, given the current state, suggests an action.

    Parameters
    ----------
    value : function of type state -> number
        The value of a current state to the player calling this AI
        function. For example, in the game of chess, this should be the
        how well a certain board layout is to the calling player.
    actions : function of type state -> [action]
        Given the current state, the function actions should return a
        list of possible actions that a player can take. If no action is
        possible this function should return an empty list.
    step : function of type state -> action -> state
        Given the current state and an action to take, the step function
        should return the new state after the action is taken.
    horizon : int
        The number of moves to look ahead, including moves made by an
        adversary.

    Returns
    -------
    type(action) or None
        The suggestion action to take, or None if no action can be taken.
    '''
    def ai(state):

        ret = max_value(horizon, value, step, actions, -inf, inf, state)
        return ret.action

    return ai


def min_value(h, value, step, actions, alpha, beta, s):
    ''' Find next with minimum value function.

    Parameters
    ----------
    h: int
        The horizon. Number of future steps to terminal condition of
        value function.
    value: function
        Function that returns the value of a (game) state.
    step: function
        Function that yields the new state after applying an action/move
        to a given state.
    actions: function
        Function that returns the possible actions/moves for a given
        board state.
    alpha: float
        Alpha parameter for alpha-beta pruning.
    beta: float
        Beta parameter for alpha-beta pruning.
    s: object
        Object describing (game) state.

    Returns
    -------
    object
        The optimal action to be taken.
    '''

    ## If we cannot make any moves, then return no move with the score.
    if len(actions(s)) is 0:
        return Move(None, value(s))

    if h is 1:
        return min(Move(a, value(step(s, a))) for a in actions(s))

    ## Convenience function, takes in a state and calls max_value.
    cofn = lambda s: max_value(h - 1, value, step, actions, alpha, beta, s)

    m = Move(None, inf)
    for a in actions(s):
        mt = Move(a, cofn(step(s, a)).value) ## temporary move variable
        if m == mt:
            m = mt
        else:
            m = min(m, mt)
        if m.value <= alpha: return m
        beta = min(beta, m.value)
    return m


def max_value(h, value, step, actions, alpha, beta, s):
    ''' Find next with minimum value function.

    Parameters
    ----------
    h: int
        The horizon. Number of future steps to terminal condition of
        value function.
    value: function
        Function that returns the value of a (game) state.
    step: function
        Function that yields the new state after applying an action/move
        to a given state.
    actions: function
        Function that returns the possible actions/moves for a given
        board state.
    alpha: float
        Alpha parameter for alpha-beta pruning.
    beta: float
        Beta parameter for alpha-beta pruning.
    s: object
        Object describing (game) state.

    Returns
    -------
    object
        The optimal action to be taken.
    '''

    ## If we cannot make any moves, then return no move with the score.
    if len(actions(s)) is 0:
        return Move(None, value(s))

    if h is 1:
        return max(Move(a, value(step(s, a))) for a in actions(s))

    ## Convenience function, takes in a state and calls min_value.
    cofn = lambda s: min_value(h - 1, value, step, actions, alpha, beta, s)

    m = Move(None, -inf)
    for a in actions(s):
        mt = Move(a, cofn(step(s, a)).value) ## temporary move variable
        if m == mt:
            m = mt
        else:
            m = max(m, mt)
        if m.value >= beta: return m
        alpha = max(alpha, m.value)
    return m


if __name__ == '__main__':

    from random import randint

    step = lambda s, a: s
    actions = lambda s: ['left', 'right']

    def value(s):

        r = randint(1, 100)
        print(r)

        return r

    ai = adversarial_search(value, actions, step, 3)
    print(ai(None))
