from matplotlib import pyplot

from counter import TimeIndependentCounter
from simulation import Simulation
from statistictests import ChiSquare
import numpy as np

"""
This file should be used to keep all necessary code that is used for the verification section in part 6
of the programming assignment. It contains task 6.2.1.
"""


def task_6_2_1():
    """
    This task is used to verify the implementation of the chi square test.
    First, 100 samples are drawn from a normal distribution. Afterwards the chi square test is run on them to see,
    whether they follow the original or another given distribution.
    """
    alpha = .1
    values = []
    np.random.seed(0)
    for _ in range(100):
        values.append(np.random.normal(0, 1))

    emp_n, emp_x = np.histogram(values, bins=100, range=(-5, 5))

    cs = ChiSquare(emp_n=emp_n, emp_x=emp_x)

    [c1, c2] = cs.test_distribution(alpha, 0, 1)

    print(f'chi_square table:{c2}')
    print(f'chi_square calculated:{c1}')

    if (c2 > c1):
        print('The H0 has not been rejected')
    else:
        print('The H0 has been rejected')

    return c2 > c1


def task_6_3_2():
    sim = Simulation()
    sim.sim_param.S = 5
    sim.sim_param.RHO = .01
    sim.sim_param.SIM_TIME = 100000

    cnt_sys_util = TimeIndependentCounter(name='sys_util')

    for _ in range(100):
        sim.reset()
        cnt_sys_util.count(sim.do_simulation().system_utilization)

    min_val = np.array(cnt_sys_util.values).min()
    max_val = np.array(cnt_sys_util.values).max()

    histogram, bins = np.histogram(cnt_sys_util.values, bins=20, range=(min_val, max_val))

    # weights = np.full(len(cnt_sys_util.values), 1.0 / float(len(cnt_sys_util.values)))
    pyplot.hist(bins[:-1], bins, alpha=0.5, rwidth=.7, weights=histogram, label='Sys. Util.')
    pyplot.title(f"ρ={sim.sim_param.RHO}")
    pyplot.ylabel("P(x)")
    pyplot.xlabel("x")
    pyplot.legend(loc='upper left')
    pyplot.xlim([0, 0.025])
    pyplot.show()
    cnt_sys_util.report()
    print('\n')

    cs = ChiSquare(emp_n=histogram, emp_x=bins)

    [c1, c2] = cs.test_distribution(0.1, cnt_sys_util.get_mean(), cnt_sys_util.get_var())

    print(f'chi_square table:{c2}')
    print(f'chi_square calculated:{c1}')

    if (c2 > c1):
        print('The H0 has not been rejected')
    else:
        print('The H0 has been rejected')

    return c2 > c1


if __name__ == '__main__':
    task_6_2_1()
    task_6_3_2()
