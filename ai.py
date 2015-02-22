## Authors: Daniel Hensley and Ryan Orendorff

from itertools import cycle
from functools import reduce
import random

from toolz import partial, take, tail


## Global definition of infinity.
inf = float('inf')


def generate(possible_actions, weight_function):
    def best_move(board):
        weight = weight_function(board)
        return random.choice([a for a, nb in possible_actions(board)])
    return best_move


def adversarial_search(value, step, horizon=3):

    return (partial(value, min_value, step, horizon),
            partial(value, max_value, step, horizon))


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


def min_value(h, value, step, s):
    ''' Find next with minimum value function.

    Parameters
    ----------
    h: int
        The horizon. Number of future steps to terminal condition of
        value function.
    value: function
        Function that returns the value of a (game) state.
    state: object
        Object describing (game) state.

    Returns
    -------
    object
        The optimal action to be taken.

    Examples
    --------
        TODO: fill in.
    '''
    if h is 1:
        return min(Move(a, value(step(s, a))) for a in actions(s))

    ## Convience function, takes in a state and calls max_value.
    cofn = lambda s: max_value(h - 1, value, step, s)

    return reduce(lambda m, a: min(m, cofn(step(s, a))),
            actions(state), Move(None, inf))


def max_value(h, value, step, s):
    ''' Find next with minimum value function.

    Parameters
    ----------
    h: int
        The horizon. Number of future steps to terminal condition of
        value function.
    value: function
        Function that returns the value of a (game) state.
    state: object
        Object describing (game) state.

    Returns
    -------
    object
        The optimal action to be taken.

    Examples
    --------
        TODO: fill in.
    '''
    if h is 1:
        return max(Move(a, value(step(s, a))) for a in actions(s))

    ## Convience function, takes in a state and calls min_value.
    cofn = lambda s: min_value(h - 1, value, step, s)

    return reduce(lambda m, a: max(m, cofn(step(s, a))),
            actions(state), Move(None, -inf))
