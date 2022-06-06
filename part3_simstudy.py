"""
This file should be used to keep all necessary code that is used for the verification section in part 3 of the
programming assignment. It contains tasks 3.2.1 and 3.2.2.
"""
from datetime import time

import numpy as np
from matplotlib import pyplot

from counter import TimeDependentCounter, TimeIndependentCounter
from histogram import TimeIndependentHistogram
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
    exp_dist = ExponentialRNS(params=arrival, the_seed=seed)
    uni_dist = UniformRNS(params=[2, 5], the_seed=seed)
    exp_values = []
    uni_values = []

    for _ in range(100000):
        exp_values.append(exp_dist.next())
        uni_values.append(uni_dist.next())

    fig, axs = pyplot.subplots(1, 2)
    fig.set_figwidth(14)

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

    bin_num = np.ceil(np.sqrt(len(uni_values)))
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

    results = {}

    for rho in [.01, .5, .8, .9]:
        results[rho] = []
        for _ in range(sim.sim_param.NO_OF_RUNS):
            sim.sim_param.RHO = rho
            sim.reset()
            results[rho].append(sim.do_simulation().system_utilization)

    fig, axs = pyplot.subplots(2, 2)
    fig.set_figwidth(10)

    for i, rho in enumerate([.01, .5, .8, .9]):
        bin_num = np.ceil(np.sqrt(len(results[rho])))
        min_val = np.array(results[rho]).min()
        max_val = np.array(results[rho]).max()
        step = (max_val - min_val) / bin_num

        histogram, bins = np.histogram(results[rho], bins=np.arange(np.floor(min_val), np.ceil(max_val), step))

        weights = np.full(len(results[rho]), 1.0 / float(len(results[rho])))
        axs[i // 2][i % 2].hist(results[rho], bins, alpha=0.5, rwidth=.7, weights=weights)
        axs[i // 2][i % 2].set_title(f"ρ={rho}")
        axs[i // 2][i % 2].set_ylabel("P(x)")
        axs[i // 2][i % 2].set_xlabel("x")

    pyplot.show()

if __name__ == '__main__':
    # task_3_2_1()
    task_3_2_2()
