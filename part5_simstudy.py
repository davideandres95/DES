import counter
from counter import TimeIndependentCounter
from simulation import Simulation
from matplotlib import pyplot
import numpy as np


"""
This file should be used to keep all necessary code that is used for the simulation section in part 5
of the programming assignment. It contains tasks 5.2.1, 5.2.2, 5.2.3 and 5.2.4.
"""


def task_5_2_1():
    """
    Run task 5.2.1. Make multiple runs until the blocking probability distribution reaches
    a confidence level alpha. Simulation is performed for 100s and 1000s and for alpha = 90% and 95%.
    """
    sim = Simulation()
    results = [None, None, None, None]

    sim.sim_param.S = 4

    sim.sim_param.RHO = 0.9

    bp_tic = counter.TimeIndependentCounter(name='block prob.')

    for idx1, sim_time in enumerate([100000, 1000000]):
        sim.sim_param.SIM_TIME = sim_time
        for idx2, alpha in enumerate([0.10, 0.05]):
            bp_tic.reset()
            runs = 0
            reached_confidence = False
            while not reached_confidence:
                runs += 1
                sim.reset()
                sim.do_simulation()
                bp_tic.count(sim.sim_result.blocking_probability)
                width = bp_tic.report_confidence_interval(alpha=alpha, print_report=False)
                if width <= (2 * sim.sim_param.EPSILON):
                    reached_confidence = True
            results[(idx1 * 2) + idx2] = runs

    print(
        'SIM TIME:  100s; ALPHA: 10%; NUMBER OF RUNS: ' + str(results[0]) + '; TOTAL SIMULATION TIME (SECONDS): ' + str(
            results[0] * 100))
    print(
        'SIM TIME:  100s; ALPHA:  5%; NUMBER OF RUNS: ' + str(results[1]) + '; TOTAL SIMULATION TIME (SECONDS): ' + str(
            results[1] * 100))
    print('SIM TIME: 1000s; ALPHA: 10%; NUMBER OF RUNS:  ' + str(
        results[2]) + '; TOTAL SIMULATION TIME (SECONDS): ' + str(results[2] * 1000))
    print('SIM TIME: 1000s; ALPHA:  5%; NUMBER OF RUNS:  ' + str(
        results[3]) + '; TOTAL SIMULATION TIME (SECONDS): ' + str(results[3] * 1000))
    return results


def task_5_2_2():
    """
    Run simulation in batches. Start the simulation with running until a customer count of n=100 or (n=1000) and
    continue to increase the number of customers by dn=n.
    Count the blocking proabability for the batch and calculate the confidence interval width of all values, that have
    been counted until now.
    Do this until the desired confidence level is reached and print out the simulation time as well as the number of
    batches.
    """
    sim = Simulation()
    results = [None, None, None, None]

    sim.sim_param.S = 4
    sim.sim_param.RHO = 0.9

    bp_tic = counter.TimeIndependentCounter(name='block prob.')

    for idx1, size in enumerate([100, 1000]):
        for idx2, alpha in enumerate([0.10, 0.05]):
            bp_tic.reset()
            sim.reset()
            batches = 0
            reached_confidence = False
            while not reached_confidence:
                sim.sim_result.reset()
                sim.counter_collection.reset()
                sim.sim_state.num_blocked_packets = 0
                sim.sim_state.num_packets = 0
                sim.sim_state.stop = False
                if batches == 0:
                    sim.do_simulation_n_limit(n=size, new_batch=False)
                else:
                    sim.do_simulation_n_limit(n=size, new_batch=True)
                bp_tic.count(sim.sim_result.blocking_probability)
                width = bp_tic.report_confidence_interval(alpha=alpha, print_report=False)
                if width <= (2 * sim.sim_param.EPSILON):
                    reached_confidence = True
                batches += 1
            results[(int(idx1) * 2) + int(idx2)] = batches

    # print and return results
    print('BATCH SIZE:  100; ALPHA: 10%; TOTAL SIMULATION TIME (SECONDS): ' + str(results[0] / 1000))
    print('BATCH SIZE:  100; ALPHA:  5%; TOTAL SIMULATION TIME (SECONDS): ' + str(results[1] / 1000))
    print('BATCH SIZE: 1000; ALPHA: 10%; TOTAL SIMULATION TIME (SECONDS): ' + str(results[2] / 1000))
    print('BATCH SIZE: 1000; ALPHA:  5%; TOTAL SIMULATION TIME (SECONDS): ' + str(results[3] / 1000))
    return results


def task_5_2_4():
    """
    Plot confidence interval as described in the task description for task 5.2.4.
    We use the function plot_confidence() for the actual plotting and run our simulation several times to get the
    samples. Due to the different configurations, we receive eight plots in two figures.
    """
    sim = Simulation()

    sim.sim_param.S = 10000

    util_tic = counter.TimeIndependentCounter(name='Utilization')

    for idx1, rho in enumerate([0.9, 0.5]):
        sim.sim_param.RHO = rho
        for idx2, sim_time in enumerate([100000, 1000000]):
            sim.sim_param.SIM_TIME = sim_time
            for idx3, alpha in enumerate([0.10, 0.05]):
                sim.sim_param.ALPHA = alpha
                results = []
                means = []
                low = []
                high = []
                for sim_id in range(0, 100):
                    util_tic.reset()
                    for run in range(0, 30):
                        sim.reset()
                        sim.do_simulation()
                        utilization = sim.sim_result.system_utilization
                        util_tic.count(utilization)
                    width = util_tic.report_confidence_interval(alpha=alpha, print_report=False)
                    results.append(width)
                    means.append(util_tic.get_mean())
                    low.append(util_tic.get_mean() - width)
                    high.append(util_tic.get_mean() + width)

                act_mean = rho
                # print(f'rho: {rho}, time: {sim_time}, alpha: {alpha}, results: low-{low} high-{high}')
                plot_confidence(sim, np.arange(0, 100), low, high, means, act_mean, "System Utilization")


def plot_confidence(sim, x, y_min, y_max, calc_mean, act_mean, ylabel):
    """
    Plot confidence levels in batches. Inputs are given as follows:
    :param sim: simulation, the measurement object belongs to.
    :param x: defines the batch ids (should be an array).
    :param y_min: defines the corresponding lower bound of the confidence interval.
    :param y_max: defines the corresponding upper bound of the confidence interval.
    :param calc_mean: is the mean calculated from the samples.
    :param act_mean: is the analytic mean (calculated from the simulation parameters).
    :param ylabel: is the y-label of the plot
    :return:
    """
    for id in x:
        pyplot.vlines(id, y_min[id], y_max[id], colors="C0")  # linestyle='dashed'

    pyplot.title(f'rho: {sim.sim_param.RHO}, time: {sim.sim_param.SIM_TIME}, alpha: {sim.sim_param.ALPHA}')
    pyplot.plot(x, np.ones(100) * act_mean, linestyle='dashed', color='C1', label='theoretical mean')
    pyplot.plot(x, np.ones(100) * np.mean(calc_mean), linestyle='dashed', color='C2', label='sample mean')
    # pyplot.scatter(x, calc_mean, marker='x')
    pyplot.ylabel(ylabel)
    middle_y = (sim.sim_param.RHO + np.mean(calc_mean)) / 2
    pyplot.ylim(middle_y - 0.1, middle_y + 0.1)
    pyplot.xlabel('sample id')
    pyplot.legend()
    pyplot.show()


if __name__ == '__main__':
    task_5_2_1()
    task_5_2_2()
    task_5_2_4()
