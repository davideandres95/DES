from __future__ import annotations
from typing import TYPE_CHECKING

from finitequeue import FiniteQueue
from packet import Packet

if TYPE_CHECKING:
    from simulation import Simulation


class SystemState(object):
    """
    This class represents the state of our system.

    It contains information about whether the server is busy and how many customers
    are waiting in the queue (buffer). The buffer represents the physical buffer or
    memory of our system, where packets are stored before they are served.

    The integer variable buffer_content represents the buffer fill status, the flag
    server_busy indicates whether the server is busy or idle.

    The simulation object is only used to determine the maximum buffer space as
    determined in its object sim_param.
    """

    def __init__(self, sim):
        """
        Create a system state object
        :param sim: simulation object for determination of maximum number of stored
        packets in buffer
        :return: system_state object
        """
        self.buffer_size = sim.sim_param.S
        self.server_busy = False
        self.buffer = FiniteQueue(sim)
        self.served_packet = None  # type: Packet
        self.last_arrival = 0
        self.sim = sim  # type: Simulation

    def add_packet_to_server(self):
        """
        Try to add a packet to the server unit.
        :return: True if server is not busy and packet has been added successfully.
        """
        if self.server_busy:
            return False
        else:
            self.server_busy = True
            self.served_packet = Packet(self.sim)
            self.served_packet.start_service()
            return True

    def add_packet_to_queue(self):
        """
        Try to add a packet to the buffer.
        :return: True if buffer/queue is not full and packet has been added successfully.
        """
        if self.buffer.add(Packet(self.sim)):
            return True
        else:
            return False

    def complete_service(self):
        """
        Reset server status to idle after a service completion.
        """
        self.server_busy = False
        self.sim.counter_collection.count_packet(self.served_packet)

    def start_service(self):
        """
        If the buffer is not empty, take the next packet from there and serve it.
        :return: True if buffer is not empty and a stored packet is being served.
        """
        if not self.buffer.is_empty():
            self.server_busy = True
            self.served_packet = self.buffer.remove()
            self.served_packet.start_service()
            return True
        else:
            return False

    def get_queue_length(self):
        return self.buffer.get_queue_length()
