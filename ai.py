## Authors: Daniel Hensley and Ryan Orendorff

from cytoolz import partial

## Global definition of infinity.
inf = float('inf')

def adversarial_search(value, prune=False, horizon=3):
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
