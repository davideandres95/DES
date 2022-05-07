from heapq import heappush, heappop
from random import randint


class EventChain(object):
    """
    This class contains a queue of events.

    Events can be inserted and removed from queue and are sorted by their time.
    Always the oldest event is removed.
    """

    def __init__(self):
        """
        Initialize variables and event chain
        """
        self.event_list = []

    def insert(self, e):
        """
        Inserts event e to the event chain. Event chain is sorted during insertion.
        :param: e is of type SimEvent

        """
        heappush(self.event_list, e)

    def remove_oldest_event(self):
        """
        Remove event with smallest timestamp (if timestamps are equal then smallest priority value i.e. highest priority event) from queue
        :return: next event in event chain
        """
        return heappop(self.event_list)


class SimEvent(object):
    """
    SimEvent represents an abstract type of simulation event.

    Contains mainly abstract methods that should be implemented in the subclasses.
    Comparison for EventChain insertion is implemented by comparing first the timestamps and then the priorities
    """

    def __init__(self, sim, timestamp):
        """
        Initialization routine, setting the timestamp of the event and the simulation it belongs to.
        """
        self.timestamp = timestamp
        self.priority = 0
        self.sim = sim  # type: Simulation

    def process(self):
        """
        General event processing routine. Should be implemented in subclass
        """
        raise NotImplementedError("Please Implement method \"process\" in subclass of SimEvent")

    def __lt__(self, other):
        """
        Comparison is made by comparing timestamps. If time stamps are equal, priorities are compared.
        """
        if self.timestamp == other.timestamp:
            return self.priority < other.priority
        else:
            return self.timestamp < other.timestamp


class CustomerArrival(SimEvent):
    """
    Defines a new customer arrival event (new packet comes into the system)
    """

    def __init__(self, sim, timestamp):
        """
        Create a new customer arrival event with given execution time.

        Priority of customer arrival event is set to 1 (second highest)
        """
        super(CustomerArrival, self).__init__(sim, timestamp)
        self.priority = 1

    def process(self):
        """
        Processing procedure of a customer arrival.

        Implement according to the task description.
        """

        sys_state = self.sim.system_state
        sim_state = self.sim.sim_state
        event_chain = self.sim.event_chain
        completion_time = sim_state.now + randint(0, 1000)
        ia_time = sim_state.now + self.sim.sim_param.IAT

        if sys_state.add_packet_to_server():  # Server is idle
            sim_state.packet_accepted()
            event_chain.insert(ServiceCompletion(sim=self.sim, timestamp=completion_time))
        else:  # system is busy
            if sys_state.add_packet_to_queue():  # Enqueue packet
                sim_state.packet_accepted()
            else:  # Drop packet
                sim_state.packet_dropped()

        # insert new CustomerArrival with IAT
        event_chain.insert(CustomerArrival(sim=self.sim, timestamp=ia_time))


class ServiceCompletion(SimEvent):
    """
    Defines a service completion event (highest priority in EventChain)
    """

    def __init__(self, sim, timestamp):
        """
        Create a new service completion event with given execution time.

        Priority of service completion event is set to 0 (highest).
        """
        super(ServiceCompletion, self).__init__(sim, timestamp)
        self.priority = 0

    def process(self):
        """
        Processing procedure of a service completion.

        Implement according to the task description
        """
        sys_state = self.sim.system_state
        event_chain = self.sim.event_chain
        sim_state = self.sim.sim_state
        completion_time = sim_state.now + randint(0, 1000)

        if sys_state.buffer_content == 0:
            sys_state.complete_service()
        elif sys_state.buffer_content > 0:
            sys_state.start_service()
            event_chain.insert(ServiceCompletion(sim=self.sim, timestamp=completion_time))


class SimulationTermination(SimEvent):
    """
    Defines the end of a simulation. (least priority in EventChain)
    """

    def __init__(self, sim, timestamp):
        """
        Create a new simulation termination event with given execution time.

        Priority of simulation termination event is set to 2 (lowest)
        """
        super(SimulationTermination, self).__init__(sim, timestamp)
        self.priority = 2

    def process(self):
        """
        Implement according to the task description.
        """
        self.sim.sim_state.stop = True
