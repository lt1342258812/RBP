from os.path import join
from scapy.all import *
import numpy as np
from math import sqrt, pi, ceil
from scipy.stats import norm
from bisect import insort_left

from Parser import Flow, Packet
import RandomSampleTime as rst
import constants as ct

# shortcuts
from constants import IN, OUT
import logging

# logging
logger = logging.getLogger('rbp')

class AdaptiveSimulator(object):
    """Simulates adaptive padding's original design on real web data."""

    def __init__(self, config):
        self.stop_on_real = bool(config.get('stop_on_real', True))

    def simulate(self, trace, timelist):
        """Adaptive padding simulation of a trace."""
        flows = {IN: Flow(IN), OUT: Flow(OUT)}
        cout_trace = len(trace)
        packet_pad = trace[2]
        for i, packet in enumerate(trace):
            logger.debug("Packet %s: %s" % (i, packet))
            flow = flows[packet.direction]
            oppflow = flows[-packet.direction]  # opposite direction
            packet.length = ct.MTU
            if (i % 2) == 0:
                self.add_padding(i, trace, flow, timelist)
            else:
                self.add_padding(i, trace, oppflow, timelist)
            # run adaptive padding in the opposite direction,
            # as if the packet was received at the other side

        # 一条流量结束,补充长度至3000
        if cout_trace < 1000:
            remain_trace = 1000 - cout_trace
            for j in range(remain_trace):  # 需要补充remain_trace条虚拟流量
                flow = flows[packet_pad.direction]
                oppflow = flows[-packet_pad.direction]  # opposite direction
                packet_pad.length = ct.MTU
                # packets = trace[10]
                if (j % 2) == 0:
                    self.add_padding_remain(packet_pad, trace, flow, timelist)
                else:
                    self.add_padding_remain(packet_pad, trace, oppflow, timelist)
        # sort race by timestamp
        trace.sort(key=lambda x: x.timestamp)

        return trace

    def add_padding(self, i, trace, flow, timelist):
        """Generate a dummy packet."""
        packet = trace[i]
        timeout = rst.Random_Iat_Sample(timelist)  # 随机获取一个IAT
        try:
            iat = self.get_iat(i, trace, flow.direction)
        except IndexError:
            self.pad_end_flow(flow)
            return
        # if iat <= 0 we do not have space for a dummy
        if not iat <= 0:
            if timeout < iat:
                logger.debug("timeout = %s  < %s = iat", timeout, iat)
                # timeout has expired
                flow.expired, flow.timeout = True, timeout
                #  生成一个随机数m
                m = np.random.randint(1, 2)
                dummy_timeout = float(timeout/m)  # 将timeout分成固定m块大小，在此期间插入m个虚拟数据包
                # the timeout has expired, we send a dummy packet
                while m > 0:
                    dummy = self.generate_dummy(packet, flow, dummy_timeout)
                    insort_left(trace, dummy)
                    m = m - 1

    def add_padding_remain(self, packets, trace, flow, timelist):
        # packet = trace[i]
        packet = packets
        timeout = rst.Random_Iat_Sample(timelist)
        flow.expired, flow.timeout = True, timeout
        dummy = self.generate_dummy(packet, flow, timeout)
        insort_left(trace, dummy)

    def get_iat(self, i, trace, direction):
        """Find previous and following packets to substract（-） their timestamps."""
        packet_0 = trace[i]
        packet_1 = self.get_next_packet(trace, i, direction)
        return packet_1.timestamp - packet_0.timestamp

    def get_next_packet(self, trace, i, direction):
        """Get the packet following the packet in position i with the same
        direction.
        """
        return trace[trace.get_next_by_direction(i, direction)]

    def pad_end_flow(self, flow):
        # AP is supposed to run continuously. So, it cannot be fairly evaluated
        # with other classifiers f we implement this funciton.
        # TODO
        pass

    def generate_dummy(self, packet, flow, timeout):
        """Set properties for dummy packet."""
        ts = packet.timestamp + timeout
        lenth = ct.MTU
        return Packet(ts, flow.direction, lenth, dummy=True)  # 时间戳、方向、数据包长度和是否为虚拟数据包
