"""
This file should be used to keep all necessary code that is used for the verification and simulation section in part 4
of the programming assignment. It contains tasks 4.2.1, 4.3.1 and 4.3.2.
"""
from matplotlib import pyplot as pyplot

from counter import TimeIndependentAutocorrelationCounter
from simulation import Simulation


def task_4_2_1():
    """
    Execute exercise 4.2.1, which is basically just a test for the auto correlation.
    """
    cnt_1 = TimeIndependentAutocorrelationCounter(name='sequence_1')
    cnt_2 = TimeIndependentAutocorrelationCounter(name='sequence_2')
    [cnt_1.count((-1) ** n) for n in range(1000)]
    for i in range(1, 1001):
        if i % 3 == 0:
            cnt_2.count(-1)
        else:
            cnt_2.count(1)
    cnt_1.report()
    cnt_2.report()

def task_4_3_1():
    """
    Run the correlation tests for given rho for all correlation counters in counter collection.
    After each simulation, print report results.
    SIM_TIME is set higher in order to avoid a large influence of startup effects
    """
    sim = Simulation()
    sim.sim_param.S = 10000
    sim.sim_param.SIM_TIME = 10000000

    for rho in [.01, .5, .8, .95]:
        print(f'####### RHO = {rho} #######\n')
        sim.sim_param.RHO = rho
        sim.reset()
        sim.do_simulation()
        sim.counter_collection.report()


def task_4_3_2():
    """
    Exercise to plot the scatter plot of (a) IAT and serving time, (b) serving time and system time
    The scatter plot helps to better understand the meaning of bit/small covariance/correlation.
    For every rho, two scatter plots are needed.
    The simulation parameters are the same as in task_4_3_1()
    """
    sim = Simulation()
    sim.sim_param.S = 10000
    sim.sim_param.SIM_TIME = 10000000

    for rho in [.01, .5, .8, .95]:
        print(f'####### RHO = {rho} #######')
        sim.sim_param.RHO = rho
        sim.reset()
        sim.do_simulation()
        iat = sim.counter_collection.cnt_iat_st.values
        st = sim.counter_collection.cnt_iat_st.values2
        sim.counter_collection.cnt_iat_st.report()

        pyplot.scatter(iat, st, s=2, c='orange')
        pyplot.title(f"Inter-arrival vs Serving Time \nρ={sim.sim_param.RHO}")
        pyplot.xlabel("IAT [ms]")
        pyplot.ylabel("ST [ms]")
        pyplot.show()

        st = sim.counter_collection.cnt_st_syst.values
        syst = sim.counter_collection.cnt_st_syst.values2
        sim.counter_collection.cnt_st_syst.report()

        pyplot.scatter(st, syst, s=2)
        pyplot.title(f"Serving vs System Time \n ρ={sim.sim_param.RHO}")
        pyplot.xlabel("ST [ms]")
        pyplot.ylabel("SYST [ms]")
        pyplot.show()


def task_4_3_3():
    """
    Exercise to plot auto correlation depending on lags. Run simulation until 10000 (or 100) packets are served.
    For the different rho values, simulation is run and the waiting time is auto correlated.
    Results are plotted for each N value in a different diagram.
    Note, that for some seeds with rho=0.01 and N=100, the variance of the auto covariance is 0 and returns an error.
    """
    sim = Simulation()
    sim.sim_param.S = 10000
    sim.sim_param.SIM_TIME = 10000000

    results = {}

    for N in [100, 10000]:
        results[N] = {}
        for rho in [.01, .5, .8, .95]:
            print(f'####### N = {N}, RHO = {rho} #######')
            sim.sim_param.RHO = rho
            sim.reset()
            sim.do_simulation_n_limit(N)
            acnt_wt = sim.counter_collection.acnt_wt
            results[N][rho] = []
            for i in range(1, 21):
                cor = acnt_wt.get_auto_cor(i)
                if cor == None:
                    print(
                        'For some seeds with rho=0.01 and N=100, the variance of the auto covariance is 0. Skipping...')
                    break
                results[N][rho].append(cor)

    for rho in results[100]:
        if results[100][rho]:
            pyplot.plot(list(range(1, 21)), results[100][rho], label=f'rho = {rho}')
    pyplot.title(f'Auto-correlation of Waiting times\nN = {100}')
    pyplot.xticks(list(range(1, 21)), list(range(1, 21)))
    pyplot.ylabel('Auto-correlation')
    pyplot.xlabel('lag')
    pyplot.legend()
    pyplot.show()

    for rho in results[10000]:
        if results[10000][rho]:
            pyplot.plot(list(range(1, 21)), results[10000][rho], label=f'rho = {rho}')
    pyplot.title(f'Auto-correlation of Waiting times\nN = {10000}')
    pyplot.xticks(list(range(1, 21)), list(range(1, 21)))
    pyplot.ylabel('Auto-correlation')
    pyplot.xlabel('lag')
    pyplot.legend()
    pyplot.show()


if __name__ == '__main__':
    task_4_2_1()
    task_4_3_1()
    task_4_3_2()
    task_4_3_3()
