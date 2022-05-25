from __future__ import annotations
import queue
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from simulation import Simulation


class FiniteQueue(object):
    """
    Class representing a finite queue representing the system buffer storing packets.

    It is a FIFO queue with finite capacity. Methods contain adding and removing packets
    as well as checking the fill status of the FIFO. Clearing the queue is done with the method flush.
    """

    def __init__(self, sim):
        """
        Initialize the finite queue
        :param sim: simulation object, that the queue belongs to
        :return: FiniteQueue object
        """
        self.sim = sim  # type: Simulation
        self.buffer = queue.Queue(maxsize=self.sim.sim_param.S)

    def add(self, packet):
        """
        Try to add a packet to the queue
        :param packet: packet which is supposed to be queued
        :return: true if packet has been enqueued, false if rejected
        """
        try:
            self.buffer.put(packet, block=False)
            return True
        except queue.Full:
            return False

    def remove(self):
        """
        Return the first packet in line and remove it from the FIFO
        :return: first packet in line
        """
        return self.buffer.get()

    def get_queue_length(self):
        """
        :return: fill status of the queue (queue length)
        """
        return self.buffer.qsize()

    def is_empty(self):
        """
        :return: true if queue is empty
        """
        return self.buffer.qsize() == 0

    def flush(self):
        """
        erase/delete all packets from the FIFO
        """
        while not self.buffer.qsize() == 0:
            self.buffer.get()
