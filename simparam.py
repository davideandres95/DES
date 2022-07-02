class SimParam(object):
    """
    Contains all important simulation parameters
    """

    def __init__(self):
        # current buffer spaces and minimal buffer spaces
        self.S_MIN = 4
        self.S = self.S_MIN  # waiting queue length
        # for part 2
        self.S_VALUES = [5, 6, 7]
        self.S_MAX = 7

        # inter-arrival-time and simulation time in ms
        self.IAT = 490
        self.SIM_TIME = 100000

        # number of runs before first evaluation
        self.NO_OF_RUNS = 1000

        # number of repeats if close to criterion (establish confidence)
        self.R = 3
        self.EPSILON = 0.0015
        self.ALPHA = 0.10

        # maximal allowed packets to drop in one run (SIM_TIME)
        self.MAX_DROPPED = 10

        # set seed for random number generation
        self.SEED = 3755457
        self.SEED_IAT = 0
        self.SEED_ST = 1

        # set desired utilization (rho)
        self.RHO = .5

    def print_sim_config(self):
        """
        Print a basic system configuration string.
        """
        print('Simulation with parameters: T_SIM = ' + str(self.SIM_TIME) + ', S = ' + str(self.S))
