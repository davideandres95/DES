# Student Name: David de Andres Hernandez
# Matriculation Number: 3755457

from simparam import SimParam
from simulation import Simulation
import random
import numpy as np
import matplotlib.pyplot as plt

"""
This file should be used to keep all necessary code that is used for the simulation study in part 1 of the programming
assignment. It contains the tasks 1.7.1, 1.7.2 and 1.7.3.

The function do_simulation_study() should be used to run the simulation routine, that is described in the assignment.
"""


def task_1_7_1():
    """
    Execute task 1.7.1 and perform a simulation study according to the task assignment.
    :return: Minimum number of buffer spaces to meet requirements.
    """
    sim_param = SimParam()
    random.seed(sim_param.SEED)
    sim = Simulation(sim_param)
    return do_simulation_study(sim)[0]


def task_1_7_2():
    """
    Execute task 1.7.2 and perform a simulation study according to the task assignment.
    :return: Minimum number of buffer spaces to meet requirements.
    """
    sim_param = SimParam()
    random.seed(sim_param.SEED)
    sim_param.SIM_TIME = 1000000
    sim_param.MAX_DROPPED = 100
    sim_param.NO_OF_RUNS = 100
    sim = Simulation(sim_param)
    return do_simulation_study(sim)[0]


def task_1_7_3():
    """
    Execute task 1.7.3.
    """
    fig, axs = plt.subplots(1, 3)
    fig.set_figwidth(21)
    sim_param = SimParam()
    random.seed(sim_param.SEED)
    sim1 = Simulation(sim_param)
    size_1, block_p_1 = do_simulation_study(sim1)
    axs[0].plot(block_p_1[size_1], label=f"100s, <10 drops in 80%, s={size_1}")

    sim_param.SIM_TIME = 1000000
    sim_param.MAX_DROPPED = 100
    sim_param.NO_OF_RUNS = 100
    random.seed(sim_param.SEED)
    sim2 = Simulation(sim_param)

    size_2, block_p_2 = do_simulation_study(sim2)
    axs[0].plot(block_p_2[size_2], label=f"1000s, <100 drops in 80%, s={size_2}")
    axs[0].set_ylim([0, 0.2])
    axs[0].set_xlim([0, 99])
    axs[0].set_title('Blocking prob for each run')
    axs[0].set_xlabel("# run")
    axs[0].set_label("P[blocking]")
    axs[0].legend()

    axs[1].hist(block_p_1[size_1], 40)
    axs[1].hist(block_p_2[size_2], 10)
    axs[1].set_title('Hist. Blocking Probability')
    axs[1].set_xlabel("P[blocking]")

    axs[2].plot(np.sort(block_p_1[size_1]),
                np.linspace(0, 1, len(block_p_1[size_1]), endpoint=False),
                label=f"100s, <10 drops in 80%, s={size_1}")

    axs[2].plot(np.sort(block_p_2[size_2]),
                np.linspace(0, 1, len(block_p_2[size_2]), endpoint=False),
                label=f"1000s, <100 drops in 80%, s={size_2}")

    axs[2].legend(loc="lower right")
    axs[2].set_xlabel("X")
    axs[2].set_ylabel("P(X<=x)")
    axs[2].set_title('CDF of the drop probability for each experiment')
    fig.show()


def do_simulation_study(sim):
    """
    Implement according to task description.
    """
    blocking_p = {}
    for queue_size in range(4, 10):
        blocking_p[queue_size] = []
        success_runs = 0
        runs = sim.sim_param.NO_OF_RUNS
        sim.sim_param.S = queue_size
        for i in range(0, runs):
            run = sim.do_simulation()
            result = run.packets_dropped
            blocking_p[queue_size].append(run.blocking_probability)
            if result < sim.sim_param.MAX_DROPPED:
                success_runs += 1
            sim.reset()

        if (success_runs / runs * 100) > 80:
            return queue_size, blocking_p


if __name__ == '__main__':
    task_1_7_1()
    task_1_7_2()
    task_1_7_3()
