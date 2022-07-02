"""
This file should be used to keep all necessary code that is used for the verification section in part 3 of the
programming assignment. It contains tasks 3.2.1 and 3.2.2.
"""
from datetime import time

import numpy as np
from matplotlib import pyplot
from scipy import stats

from counter import TimeIndependentCounter
from rng import RNG, ExponentialRNS, UniformRNS
from simulation import Simulation

RHO = 0.5
arrival = 0.001
seed = 3755457


def task_3_2_1():
    """
    This function plots two histograms for verification of the random distributions.
    One histogram is plotted for a uniform distribution, the other one for an exponential distribution.
    """
    plot_random_distribution_histograms()


def plot_random_distribution_histograms(bin_num=None):
    exp_dist = ExponentialRNS(lambda_x=arrival, the_seed=seed)
    uni_dist = UniformRNS(a=2, b=5, the_seed=seed)
    exp_values = []
    uni_values = []

    for _ in range(100000):
        exp_values.append(exp_dist.next())
        uni_values.append(uni_dist.next())

    fig, axs = pyplot.subplots(1, 2)
    fig.set_figwidth(20)

    if bin_num == None:
        bin_num = np.ceil(np.sqrt(len(exp_values)))
    min_val = np.array(exp_values).min()
    max_val = np.array(exp_values).max()
    step = (max_val - min_val) / bin_num

    histogram, bins = np.histogram(exp_values, bins=np.arange(np.floor(min_val), np.ceil(max_val), step))

    weights = np.full(len(exp_values), 1.0 / float(len(exp_values)))
    axs[0].hist(exp_values, bins, alpha=0.5, rwidth=.7, weights=weights)
    axs[0].set_title(f"Exponential distribution with λ={arrival}")
    axs[0].set_ylabel("P(x)")
    axs[0].set_xlabel("x")

    if bin_num == None:
        bin_num = np.ceil(np.sqrt(len(exp_values)))
    min_val = np.array(uni_values).min()
    max_val = np.array(uni_values).max()
    step = (max_val - min_val) / bin_num

    histogram, bins = np.histogram(uni_values, bins=np.arange(np.floor(min_val), np.ceil(max_val), step))

    weights = np.full(len(uni_values), 1.0 / float(len(uni_values)))
    axs[1].hist(uni_values, bins, alpha=0.5, rwidth=.7, weights=weights)
    axs[1].set_title(f"Uniform distribution with [a, b]=[2, 5]")
    axs[1].set_ylabel("P(x)")
    axs[1].set_xlabel("x")
    pyplot.show()

def task_3_2_2():
    """
    Here, we execute task 3.2.2 and print the results to the console.
    The first result string keeps the results for 100s, the second one for 1000s simulation time.
    """
    sim = Simulation()
    sim.sim_param.S = 5
    sim.sim_param.SIM_TIME = 100000

    print("####### SIM_TIME = 100s #######")

    for rho in [.01, .5, .8, .9]:
        sim.sim_param.RHO = rho
        sim.reset()
        sim.do_simulation()
        sim.counter_collection.cnt_sys_util.report()

    print("####### SIM_TIME = 1000s #######")

    sim.sim_param.SIM_TIME = 1000000
    for rho in [.01, .5, .8, .9]:
        sim.sim_param.RHO = rho
        sim.reset()
        sim.do_simulation()
        sim.counter_collection.cnt_sys_util.report()


def task_3_3_3():
    sim = Simulation()
    sim.sim_param.S = 5
    sim.sim_param.RHO = .01
    sim.sim_param.SIM_TIME = 100000

    cnt_sys_util = TimeIndependentCounter(name='sys_util')

    for _ in range(sim.sim_param.NO_OF_RUNS):
        sim.reset()
        cnt_sys_util.count(sim.do_simulation().system_utilization)

    bin_num = np.ceil(np.sqrt(len(cnt_sys_util.values)))
    min_val = np.array(cnt_sys_util.values).min()
    max_val = np.array(cnt_sys_util.values).max()
    step = (max_val - min_val) / bin_num

    histogram, bins = np.histogram(cnt_sys_util.values, bins=np.arange(np.floor(min_val), np.ceil(max_val), step))

    weights = np.full(len(cnt_sys_util.values), 1.0 / float(len(cnt_sys_util.values)))
    pyplot.hist(bins[:-1], bins, alpha=0.5, rwidth=.7, weights=histogram, label='Sys. Util.')
    pyplot.title(f"ρ={sim.sim_param.RHO}")
    pyplot.ylabel("P(x)")
    pyplot.xlabel("x")
    pyplot.legend(loc='upper left')
    ax2 = pyplot.twinx()
    plot_gaussian(cnt_sys_util.get_mean(), cnt_sys_util.get_stddev())
    ax2.set_ylim([0, 270])
    ax2.get_yaxis().set_visible(False)
    pyplot.xlim([0, 0.025])
    ax2.legend(loc='upper right')
    pyplot.show()

    cnt_sys_util.report()


def task_3_3_4():
    sim = Simulation()
    sim.sim_param.S = 1000000
    sim.sim_param.SIM_TIME = 1000000

    print("####### S = 1000000 SIM_TIME = 1000s #######")

    for rho in [.01, .5, .8, .9]:
        sim.sim_param.RHO = rho
        sim.reset()
        sim.do_simulation()
        sim.counter_collection.cnt_sys_util.report()

    print("####### S = 1000000 SIM_TIME = 10000s #######")

    sim.sim_param.SIM_TIME = 10000000
    for rho in [.01, .5, .8, .9]:
        sim.sim_param.RHO = rho
        sim.reset()
        sim.do_simulation()
        sim.counter_collection.cnt_sys_util.report()


def gauss(x, mean, sigma):
    return (1 / (sigma * np.sqrt(2 * np.pi))) * np.exp(-0.5 * np.square((x - mean) / sigma))


def plot_gaussian(mean, sigma):
    x_data = np.arange(0, 0.025, 0.00001)

    ## y-axis as the gaussian
    y_data = gauss(x_data, mean, sigma)
    ## plot data
    pyplot.plot(x_data, y_data, label='Gaussian', color='orange')


if __name__ == '__main__':
    # task_3_2_1()
    # task_3_2_2()
    # task_3_3_3()
    task_3_3_4()
