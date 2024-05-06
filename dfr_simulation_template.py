#!/usr/bin/env python
# -*- coding: utf-8 -*-
##
# @file     dfr_simulation.py
# @author   Kyeong Soo (Joseph) Kim <kyeongsoo.kim@gmail.com>
# @date     2020-05-15
#           2023-04-11
#           2024-04-25
#
# @brief Skeleton code for the simulation of video streaming to investigate the
#        impact of packet losses on the quality of video streaming based on
#        decodable frame rate (DFR)
#


import argparse
import math
import numpy as np
import os
import sys

sys.path.insert(0, os.getcwd())  # assume that your own modules in the current directory
from conv_interleave import conv_interleave, conv_deinterleave
from sgm_generate import sgm_generate


def dfr_simulation(
        random_seed,
        num_frames,
        loss_probability,
        video_trace,
        fec,
        ci):
    np.random.seed(random_seed)  # set random seed

    # N.B.: Obtain the information of the whole frames to create a loss
    # sequence in advance due to the optional convolutional
    # interleaving/deinterleaving.
    with open(video_trace, "r") as f:
        lines = f.readlines()[1:num_frames + 1]  # the first line is a comment.

    f_number = np.empty(num_frames, dtype=np.uint)
    f_type = [''] * num_frames
    f_pkts = np.empty(num_frames, dtype=np.uint)  # the number of packets per frame
    for i in range(num_frames):
        f_info = lines[i].split()
        f_number[i] = int(f_info[0])  # str -> int
        f_type[i] = f_info[2]
        f_pkts[i] = math.ceil(int(f_info[3]) / (188 * 8))

    # symbol loss sequence
    p = 1e-4
    q = p * (1.0 - loss_probability) / loss_probability
    n_pkts = sum(f_pkts)  # the number of packets for the whole frames
    if ci:
    # apply convolutional interleaving/deinterleaving.
    # N.B.:
    # 1. Append 2244 zeros before interleaving.
    # 2. Interleaved sequence experiences symbol losses.
    # 3. Remove leading 2244 elements after deinterleaving.

    # TODO: Implement.

    else:
    # TODO: Implement.

    # initialize variables.
    idx = -1
    for j in range(2):
        idx = f_type.index('I', idx + 1)
    gop_size = f_number[idx]  # N.B.: the frame number of the 2nd I frame is GOP size.
    num_b_frames = f_number[1] - f_number[0] - 1  # between I and the 1st P frames
    i_frame_number = -1  # the last decodable I frame number
    p_frame_number = -1  # the last decodable P frame number
    num_frames_decoded = 0
    num_pkts_received = 0
    num_frames_decoded = 0
    num_frames_received = 0

    # main loop
    for i in range(num_frames):
        # frame loss
        pkt_losses = sum(losses[num_pkts_received:num_pkts_received + f_pkts[i]])
        num_pkts_received += f_pkts[i]
        if fec:
        # TODO: Set "frame_loss" based on "pkt_losses" with FEC.

        else:
        # TODO: Set "frame_loss" based on "pkt_losses" without FEC.

        # frame decodability
        if not frame_loss:  # see the fec-dependent handling of "frame_loss" above.
            match f_type[i]:
                case 'I':
                # TODO: Implement.

                case 'P':
                # TODO: Implement.

                case 'B':
                # TODO: Implement.

                case _:
                    sys.exit("Unkown frame type is detected.")

    return num_frames_decoded / num_frames  # DFR


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-N",
        "--num_frames",
        help="number of frames to simulate; default is 10000",
        default=10000,
        type=int)
    parser.add_argument(
        "-P",
        "--loss_probability",
        help="overall loss probability; default is 0.1",
        default=0.1,
        type=float)
    parser.add_argument(
        "-R",
        "--random_seed",
        help="seed for numpy random number generation; default is 777",
        default=777,
        type=int)
    parser.add_argument(
        "-V",
        "--video_trace",
        help="video trace file; default is 'silenceOfTheLambs_verbose'",
        default="silenceOfTheLambs_verbose",
        type=str)

    # convolutional interleaving/deinterleaving (CI); default is False
    parser.add_argument('--ci', dest='ci', action='store_true')
    parser.add_argument('--no-ci', dest='ci', action='store_false')
    parser.set_defaults(ci=False)

    # forward error correction (FEC); default is False (i.e., not using FEC)
    parser.add_argument('--fec', dest='fec', action='store_true')
    parser.add_argument('--no-fec', dest='fec', action='store_false')
    parser.set_defaults(fec=False)

    args = parser.parse_args()

    # set variables using command-line arguments
    num_frames = args.num_frames
    loss_model = args.loss_model
    loss_probability = args.loss_probability
    video_trace = args.video_trace
    ci = args.ci
    fec = args.fec
    trace = args.trace

    # run simulation and display the resulting DFR.
    dfr = dfr_simulation(
        args.random_seed,
        args.num_frames,
        args.loss_probability,
        args.video_trace,
        args.fec,
        args.ci)
    print(f"Decodable frame rate = {dfr:.4E}\n")