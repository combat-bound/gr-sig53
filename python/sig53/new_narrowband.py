#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2025 Combat Bound, LLC.
#
# SPDX-License-Identifier: GPL-3.0-or-later
#


import numpy
from gnuradio import gr

class new_narrowband(gr.sync_block):
    """
    docstring for block new_narrowband
    """
    def __init__(self, vector_size=1024, class_name="16qam", dataset_length=1024 * 1024 * 500, fft_size=1024, impairment_level=1, sample_rate=10e6):
        gr.sync_block.__init__(self,
            name="new_narrowband",
            in_sig=None,
            out_sig=[<+numpy.float32+>, ])


    def work(self, input_items, output_items):
        out = output_items[0]
        # <+signal processing here+>
        out[:] = whatever
        return len(output_items[0])
