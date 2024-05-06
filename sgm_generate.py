#!/usr/bin/env python
# -*- coding: utf-8 -*-
##
# @file     sgm_generate.py
# @author   Kyeong Soo (Joseph) Kim <kyeongsoo.kim@gmail.com>
# @date     2020-03-25
#           2023-04-10
#
# @brief    A function for generating loss pattern based on the simple
#           Guilbert model (SGM).
#

import numpy as np
from numba import jit


@jit # optional: optimize using numba
def sgm_generate(R, L, p, q):
    """
    Generate a binary sequence of 0 (GOOD) and 1 (BAD) of length 'l'
    from the SGM specified by transition probabilites 'p' (GOOD->BAD)
    and 'q' (BAD->GOOD).

    This function assumes that the SGM starts in GOOD (0) state.

    Examples:

    seq = sgm_generate(100, 0.95, 0.9)
    """

    np.random.seed(R) # set the random seed
    seq = np.zeros(L, dtype=np.int64) # as an integer array

    # check transition probabilites
    if p < 0 or p > 1:
        print("The value of the transition probability p is not valid.")
        return
    elif q < 0 or q > 1:
        print("The value of the transition probability q is not valid.")
        return
    else:
        tr = [p, q]

    # create a random sequence for state changes
    statechange = np.random.rand(L)

    # Assume that we start in GOOD state (0).
    state = 0

    # main loop
    for i in range(L):
        if statechange[i] <= tr[state]:
            # transition into the other state
            state ^= 1
        # add a binary value to output
        seq[i] = state

    return seq


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-R",
        "--random_seed",
        help="seed for numpy random number generation; default is 777",
        default=777,
        type=int)
    parser.add_argument(
        "-L",
        "--length",
        help="the length of the loss pattern to be generated; default is 10",
        default=10,
        type=int)
    parser.add_argument(
        "-p",
        help="GOOD to BAD transition probability; default is 0.95",
        default=0.95,
        type=float)
    parser.add_argument(
        "-q",
        help="BAD to GOOD transition probability; default is 0.9",
        default=0.9,
        type=float)
    args = parser.parse_args()
    res = sgm_generate(args.random_seed, args.length, args.p, args.q)
    if res is not None:
        print(res)
