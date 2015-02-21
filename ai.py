## Authors: Daniel Hensley and Ryan Orendorff

from itertools import cycle

from toolz import partial, take

## Global definition of infinity.
inf = float('inf')

def generate(possible_actions, weight_function):
    def best_move(board):
        weight = weight_function(board)
        for action, new_board in possible_actions(board):
            new_weight = weight_function(new_board)
            if new_weight >= weight:
                return action
    return best_move


def adversarial_search(value, prune=False, horizon=3):
    queue = take(horizon, cycle([max, min]))
    if prune:
        return (partial(value, min_value_prune, horizon),
                partial(value, max_value_prune, horizon))
    else:
        return (partial(value, min_value, horizon),
                partial(value, max_value, horizon))


def min_value(horizon, value, state):
    ''' Find next with minimum value function.

    Parameters
    ----------
    horizon: int
        Number of future steps to terminal condition of value function.
    state: object
        Object describing (game) state.
    value: function
        Function that returns the value of a (game) state.

    Returns
    -------
    object
        The optimal action to be taken.

    Examples
    --------
        TODO: fill in.
    '''
    if horizon == 0:
        return value(state)

    v = inf
    for a in actions(state):
        next_state = a(state)
        v = min(v, max_value(horizon - 1,  value, next_state))

    return v


def max_value(horizon, value, state):
    ''' Find next with minimum value function.

    Parameters
    ----------
    horizon: int
        Number of future steps to terminal condition of value function.
    state: object
        Object describing (game) state.
    value: function
        Function that returns the value of a (game) state.

    Returns
    -------
    object
        The optimal action to be taken.

    Examples
    --------
        TODO: fill in.
    '''
    if horizon == 0:
        return value(state)

    v = -inf
    for a in actions(state):
        next_state = a(state)
        v = min(v, min_value(horizon - 1, value, next_state))

    return v


def min_value_prune(horizon, state, value):
    pass


def max_value_prune(horizon, state, value):
    pass
