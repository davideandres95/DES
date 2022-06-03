# Student Name: David de Andres Hernandez
# Matriculation Number: 3755457

from simparam import SimParam
from simulation import Simulation
from histogram import TimeIndependentHistogram
from counter import TimeIndependentCounter
import random

"""
This file should be used to keep all necessary code that is used for the simulation study in part 2 of the programming
assignment. It contains the tasks 2.7.1 and 2.7.2.

The function do_simulation_study() should be used to run the simulation routine, that is described in the assignment.
"""


def task_2_7_1():
    """
    Here, you should execute task 2.7.1 (and 2.7.2, if you want).
    """
    sim_param = SimParam()
    sim_param.S_VALUES = [5, 6, 7]
    random.seed(sim_param.SEED)
    sim = Simulation(sim_param)
    do_simulation_study(sim, True, True)


def task_2_7_2():
    """
    Here, you can execute task 2.7.2 if you want to execute it in a separate function
    """
    sim_param = SimParam()
    sim_param.S_VALUES = [5, 6, 7]
    sim_param.SIM_TIME = 1000000
    random.seed(sim_param.SEED)
    sim = Simulation(sim_param)
    do_simulation_study(sim, True, True)


def do_simulation_study(sim, print_queue_length=False, print_waiting_time=True):
    """
    This simulation study is different from the one made in assignment 1. It is mainly used to gather and visualize
    statistics for different buffer sizes S instead of finding a minimal number of spaces for a desired quality.
    For every buffer size S (which ranges from 5 to 7), statistics are printed (depending on the input parameters).
    Finally, after all runs, the results are plotted in order to visualize the differences and giving the ability
    to compare them. The simulations are run first for 100s, then for 1000s. For each simulation time, two diagrams are
    shown: one for the distribution of the mean waiting times and one for the average buffer usage
    :param sim: the simulation object to do the simulation
    :param print_queue_length: print the statistics for the queue length to the console
    :param print_waiting_time: print the statistics for the waiting time to the console
    """
    results = {'waiting_time': {}, 'queue_length': {}}
    for queue_size in sim.sim_param.S_VALUES:
        runs = sim.sim_param.NO_OF_RUNS
        sim.sim_param.S = queue_size
        results['waiting_time'][queue_size] = {}
        results['queue_length'][queue_size] = {}
        results['waiting_time'][queue_size]['values'] = TimeIndependentCounter(name='waiting_time')
        results['queue_length'][queue_size]['values'] = TimeIndependentCounter(name='queue_length')
        results['waiting_time'][queue_size]['hist'] = TimeIndependentHistogram(sim, 'w')
        results['queue_length'][queue_size]['hist'] = TimeIndependentHistogram(sim, 'q')
        for i in range(0, runs):
            run = sim.do_simulation()
            results['waiting_time'][queue_size]['hist'].count(run.mean_waiting_time)
            results['waiting_time'][queue_size]['values'].count(run.mean_waiting_time)
            results['queue_length'][queue_size]['hist'].count(run.mean_queue_length)
            results['queue_length'][queue_size]['values'].count(run.mean_queue_length)
            sim.reset()
        if print_queue_length:
            print(
                f'The mean queue length for S={queue_size} is {results["queue_length"][queue_size]["values"].get_mean()}')
            print(
                f'The variance of the queue length for S={queue_size} is {results["queue_length"][queue_size]["values"].get_var()}')
        if print_waiting_time:
            print(
                f'The mean waiting time for S={queue_size} is {results["waiting_time"][queue_size]["values"].get_mean()}s')

    for key, value in results['waiting_time'].items():
        sim.sim_param.S = key
        value['hist'].report()
        if key == 7:
            value['hist'].plot(diag_type="line", show_plot=True)
        else:
            value['hist'].plot(diag_type="line", show_plot=False)
    positions = ['left', 'center', 'right']
    for (key, value), pos in zip(results['queue_length'].items(), positions):
        sim.sim_param.S = key
        value['hist'].report()
        if key == 7:
            value['hist'].plot(diag_type="side-by-side", show_plot=True, pos=pos)
        else:
            value['hist'].plot(diag_type="side-by-side", show_plot=False, pos=pos)
    return results

if __name__ == '__main__':
    task_2_7_1()
    task_2_7_2()
