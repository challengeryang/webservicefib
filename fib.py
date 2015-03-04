#!/usr/bin/python
#
# author: Bo Yang
#

"""
Fibonacci methods
"""

HELP_MESSAGE = "Please input non negative integer"

def fib():
    """ generate Fibonacci numbers """
    curr_val, next_val = 0, 1
    while True:
        yield curr_val
        curr_val, next_val = next_val, curr_val + next_val

def _fib_sequence(num):
    """
    generate sequence of first 'num' Fibonacci numbers 
    """
    # TODO: set a proper maximum value to avoid big number
    # slow down the performance and use up memory
    if num == 0:
         return ' '
    fib_seq = []
    for idx, fib_val in enumerate(fib()):
        fib_seq.append(str(fib_val))
        if idx == num - 1:
            break
    return ' '.join(fib_seq)

def fib_sequence_wapper(val):
    """
    wapper function for _fib_sequence
    """
    num = 0

    try:
        # whether it's int or float
        num = int(val)
    except (TypeError, ValueError):
        return HELP_MESSAGE

    # only integer is expected
    if str(val).find('.') >= 0:
        return HELP_MESSAGE
    # only positive integer is expected
    elif num < 0:
        return HELP_MESSAGE
    # finally, get the valid number
    else:
        return _fib_sequence(num)
