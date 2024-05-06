#!/usr/bin/env python
# -*- coding: utf-8 -*-
##
# @file     interleaved_loss_seq.py
# @author   Kyeong Soo (Joseph) Kim <kyeongsoo.kim@gmail.com>
# @date     2023-04-17
#
# @brief An example of interleaved loss sequence
#


import numpy as np
import os
import sys
sys.path.insert(0, os.getcwd()) # "conv_interleave.py" is in the current directory
from conv_interleave import conv_interleave, conv_deinterleave, print_binary


x1 = np.concatenate([np.ones(2040), np.zeros(2244)]).astype(int)
# input symbols (ones) of 10 DVB packets followed by zeros to clear
# the shift registers in the interleaver
d1 = [int(i) for i in "17,34,51,68,85,102,119,136,153,170,187".split(',')]
d2 = d1[::-1]
x2 = conv_interleave(x1, d1) # convolved symbols
loss_seq1 = np.random.randint(2, size=len(x2))  # loss -> 1
y = x2*loss_seq1 # symbols affected by losses
z = conv_deinterleave(y, d2)
loss_seq2 = z[2244:] # remove prepended zeros (i.e., those from SRSs)
print_binary(loss_seq2, "Interleaved loss sequence")