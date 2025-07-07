#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2025 Combat Bound, LLC.
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

import numpy as np
import pmt

from gnuradio import gr
from torchsig.datasets.narrowband import NewNarrowband
from torchsig.datasets.dataset_metadata import NarrowbandMetadata


class new_narrowband(gr.sync_block):
    """
    docstring for block new_narrowband
    """
    def __init__(self,
                 vector_size=1024,
                 class_name="16qam",
                 dataset_length=1024 * 1024 * 5,
                 fft_size=1024,
                 impairment_level=1,
                 sample_rate=10e6,
                 repeat=False):
        gr.sync_block.__init__(self,
            name="new_narrowband",
            in_sig=None,
            out_sig=[(np.complex64, vector_size)]
        )
        # if an attribute with the same name as a parameter is found,
        # a callback is registered (properties work, too).
        self.vector_size = vector_size
        self.class_name = class_name
        self.dataset_length = dataset_length
        self.fft_size = fft_size
        self.impairment_level = impairment_level
        self.sample_rate = sample_rate
        self.repeat = repeat
        # Internal state tracking
        self.seek_offset = 0
        self.signals = None
        # Message ports
        self.dataset_label_port_name = 'datasetLabel'
        self.message_port_register_out(pmt.intern(self.dataset_label_port_name))


    def next_dataset(self):
        self.signals, labels = next(self.dataset)
        self.message_port_pub(pmt.intern(self.dataset_label_port_name),
                              pmt.to_pmt(labels))

    def start(self):
        spec = NarrowbandMetadata(
                int(self.dataset_length),
                int(self.fft_size),
                int(self.impairment_level),
                sample_rate=self.sample_rate,
                class_list=[self.class_name]
            )
        self.dataset = NewNarrowband(spec)
        self.next_dataset()

    def __next__(self):
        assert self.signals is not None, "Block is not started"
        sample = np.empty(self.vector_size, dtype=np.complex64)
        remaining = len(self.signals) - self.seek_offset
        if remaining > self.vector_size:
            sample[:] = self.signals[self.seek_offset:self.vector_size + self.seek_offset]
            self.seek_offset += self.vector_size
        elif self.repeat:
            sample[:remaining] = self.signals[self.seek_offset:]
            del self.signals
            self.next_dataset()
            self.seek_offset = self.vector_size - remaining
            sample[remaining:] = self.signals[:self.seek_offset]
        else:
            raise StopIteration()
        return sample

    def work(self, input_items, output_items):
        """
        """
        try:
            output_items[0][:self.vector_size] = next(self)
            return self.vector_size
        except StopIteration:
            return -1
