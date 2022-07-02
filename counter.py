import numpy as np
from scipy.stats import t, skew
from collections import deque


class Counter(object):
    """
    Counter class is an abstract class, that counts values for statistics.

    Values are added to the internal array. The class is able to generate mean value, variance and standard deviation.
    The report function prints a string with name of the counter, mean value and variance.
    All other methods have to be implemented in subclasses.
    """

    def __init__(self, name="default"):
        """
        Initialize a counter with a name.
        The name is only for better distinction between counters.
        :param name: identifier for better distinction between various counters
        """
        self.name = name
        self.values = []

    def count(self, *args):
        """
        Count values and add them to the internal array.
        Abstract method - implement in subclass.
        """
        raise NotImplementedError("Please Implement this method")

    def reset(self, *args):
        """
        Delete all values stored in internal array.
        """
        self.values = []

    def get_mean(self):
        """
        Returns the mean value of the internal array.
        Abstract method - implemented in subclass.
        """
        raise NotImplementedError("Please Implement this method")

    def get_var(self):
        """
        Returns the variance of the internal array.
        Abstract method - implemented in subclass.
        """
        raise NotImplementedError("Please Implement this method")

    def get_stddev(self):
        """
        Returns the standard deviation of the internal array.
        Abstract method - implemented in subclass.
        """
        raise NotImplementedError("Please Implement this method")

    def report(self):
        """
        Print report for this counter.
        """
        if len(self.values) != 0:
            print('Name: ' + str(self.name) + ', Mean: ' + str(self.get_mean()) + ', Variance: ' + str(self.get_var()))
        else:
            print('List for creating report is empty. Please check.')


class TimeIndependentCounter(Counter):
    """
    Counter for counting values independent of their duration.

    As an extension, the class can report a confidence interval and check if a value lies within this interval.
    """

    def __init__(self, name="default"):
        """
        Initialize the TIC object.
        """
        super(TimeIndependentCounter, self).__init__(name)

    def count(self, *args):
        """
        Add a new value to the internal array. Parameters are chosen as *args because of the inheritance to the
        correlation counters.
        :param: *args is the value that should be added to the internal array
        """
        self.values.append(args[0])

    def get_mean(self):
        """
        Return the mean value of the internal array.
        """
        if len(self.values) <= 0:
            raise RuntimeError("No values stored in the counter. Abort.")
        else:
            return np.mean(self.values)

    def get_var(self):
        """
        Return the variance of the internal array.
        Note, that we take the estimated variance, not the exact variance.
        """
        if len(self.values) <= 0:
            raise RuntimeError("No values stored in the counter. Abort.")
        else:
            return np.var(self.values, ddof=1)

    def get_stddev(self):
        """
        Return the standard deviation of the internal array.
        """
        return np.std(self.values, ddof=1)

    def get_skewness(self):
        """
        :return: the sample skewness of a data set.
        """
        return skew(self.values)

    def report_confidence_interval(self, alpha=0.05, print_report=True):
        """
        Report a confidence interval with given significance level.
        This is done by using the t-table provided by scipy.
        :param alpha: is the significance level (default: 5%)
        :param print_report: enables an output string
        :return: half width of confidence interval h
        """
        if (alpha >= 0 and alpha <= 1):
            variance = np.sqrt(self.get_var() / len(self.values))
            t_alpha_half = t.ppf(float(1 - (alpha / 2)), len(self.values) - 1)
            interval = variance * t_alpha_half
            if print_report:
                print(f'The half width of confidence interval is: {interval}')
            return interval
        else:
            raise ValueError('The level of signigicance must belong to [0,1]')

    def is_in_confidence_interval(self, x, alpha=0.05):
        """
        Check if sample x is in confidence interval with given significance level.
        :param x: is the sample
        :param alpha: is the significance level
        :return: true, if sample is in confidence interval
        """
        half_width = self.report_confidence_interval(alpha)
        mean = self.get_mean()
        if x >= mean - half_width and x <= mean + half_width:
            return True
        else:
            return False

    def report_bootstrap_confidence_interval(self, alpha=0.05, resample_size=5000, print_report=True):
        """
        Report bootstrapping confidence interval with given significance level.
        This is done with the bootstrap method. Hint: use numpy.random.choice for resampling
        :param alpha: significance level
        :param resample_size: resampling size
        :param print_report: enables an output string
        :return: lower and upper bound of confidence interval
        """
        deltas = []
        for i in range(resample_size):
            samples = np.random.choice(self.values, len(self.values), replace=True)
            deltas.append(np.mean(samples) - self.get_mean())
        sorted_deltas = sorted(deltas)

        lower = self.get_mean() - np.quantile(sorted_deltas, 1 - (alpha / 2))
        upper = self.get_mean() - np.quantile(sorted_deltas, alpha / 2)

        if print_report:
            # print('Upper index: ' + str(index1) + ' Lower index: ' + str(index2))
            print('The bootstrap confidence interval is: [' + str(lower) + ', ' + str(upper) + ']')
        return lower, upper

    def is_in_bootstrap_confidence_interval(self, x, resample_size=5000, alpha=0.05):
        """
        Check if sample x is in bootstrap confidence interval with given resample_size and significance level.
        :param x: is the sample
        :param resample_size: resample size
        :param alpha: is the significance level
        :return: true, if sample is in confidence interval
        """
        lower, upper = self.report_bootstrap_confidence_interval(alpha=alpha, resample_size=resample_size)
        if x >= lower and x <= upper:
            return True
        else:
            return False


class TimeDependentCounter(Counter):
    """
    Counter, that counts values considering their duration as well.

    Methods for calculating mean, variance and standard deviation are available.
    """

    def __init__(self, sim, name="default"):
        """
        Initialize TDC with the simulation it belongs to and the name.
        :param: sim is needed for getting the current simulation time.
        :param: name is an identifier for better distinction between multiple counters.
        """
        super(TimeDependentCounter, self).__init__(name)
        self.sim = sim
        self.first_timestamp = 0
        self.last_timestamp = 0
        self.sum_power_two = []  # second moment used for variance calculation

    def count(self, value):
        """
        Adds new value to internal array.
        Duration from last to current value is considered.
        """

        dt = self.sim.sim_state.now - self.last_timestamp
        if dt < 0:
            print('Error in calculating time dependent statistics. Current time is smaller than last timestamp.')
            raise ValueError
        # Second moment
        self.sum_power_two.append(value * value * dt)
        # First moment
        self.values.append(value * dt)
        self.last_timestamp = self.sim.sim_state.now

    def get_mean(self):
        """
        Return the mean value of the counter, normalized by the total duration of the simulation.
        """
        return float(sum(self.values)) / float((self.last_timestamp - self.first_timestamp))

    def get_var(self):
        """
        Return the variance of the TDC.
        """
        dt = self.last_timestamp - self.first_timestamp
        return float(sum(self.sum_power_two)) / float(dt) - self.get_mean() * self.get_mean()

    def get_stddev(self):
        """
        Return the standard deviation of the TDC.
        """
        return np.sqrt(self.get_var())

    def reset(self):
        """
        Reset the counter to its initial state.
        """
        self.first_timestamp = self.sim.sim_state.now
        self.last_timestamp = self.sim.sim_state.now
        self.sum_power_two = []
        Counter.reset(self)


class TimeIndependentCrosscorrelationCounter(TimeIndependentCounter):
    """
    Counter that is able to calculate cross correlation (and covariance).
    """

    def __init__(self, name="default"):
        """
        Crosscorrelation counter contains three internal counters containing the variables
        :param name: is a string for better distinction between counters.
        """
        super(TimeIndependentCrosscorrelationCounter, self).__init__(name)
        self.values2 = []
        self.prod = []

    def reset(self):
        """
        Reset the TICCC to its initial state.
        """
        TimeIndependentCounter.reset(self)
        self.values2 = []
        self.prod = []

    def count(self, x, y):
        """
        Count two values for the correlation between them. They are added to the two internal arrays.
        """
        self.values.append(x)
        self.values2.append(y)
        self.prod.append(x * y)

    def get_cov(self):
        """
        Calculate the covariance between the two internal arrays x and y.
        :return: cross covariance
        """
        return np.mean(self.prod) - np.mean(self.values) * np.mean(self.values2)

    def get_cor(self):
        """
        Calculate the correlation between the two internal arrays x and y.
        :return: cross correlation
        """
        var_x = np.var(self.values, ddof=1)
        var_y = np.var(self.values2, ddof=1)
        return self.get_cov() / np.sqrt(var_x * var_y)

    def report(self):
        """
        Print a report string for the TICCC.
        """
        print('Name: ' + self.name + '; covariance = ' + str(self.get_cov()) + '; correlation = ' + str(self.get_cor()))


class TimeIndependentAutocorrelationCounter(TimeIndependentCounter):
    """
    Counter, that is able to calculate auto correlation with given lag.
    """

    def __init__(self, name="default", max_lag=10):
        """
        Create a new auto correlation counter object.
        :param name: string for better distinction between multiple counters
        :param max_lag: maximum available lag (defaults to 10)
        """
        super(TimeIndependentAutocorrelationCounter, self).__init__(name)
        self.max_lag = max_lag

    def reset(self):
        """
        Reset the counter to its original state.
        """
        TimeIndependentCounter.reset(self)
        self.max_lag = 10

    def count(self, x):
        """
        Add new element x to counter.
        """
        self.values.append(x)

    def get_auto_cov(self, lag):
        """
        Calculate the auto covariance for a given lag.
        :return: auto covariance
        """
        shift = deque(self.values)
        shift.rotate(lag)
        prod = [x * y for x, y in zip(self.values, list(shift))]
        return np.mean(prod) - np.mean(self.values) * np.mean(list(shift))

    def get_auto_cor(self, lag):
        """
        Calculate the auto correlation for a given lag.
        :return: auto correlation
        """
        shift = deque(self.values)
        shift.rotate(lag)
        var_x = np.var(self.values, ddof=1)
        var_y = np.var(list(shift), ddof=1)
        if (var_x != 0.0 and var_y != 0.0):
            return self.get_auto_cov(lag) / np.sqrt(var_x * var_y)
        else:
            print(f'Warning, the variance is var_x = {var_x}, var_y = {var_y}')

    def set_max_lag(self, max_lag):
        """
        Change maximum lag. Cycle length is set to max_lag + 1.
        """
        self.max_lag = max_lag

    def report(self):
        """
        Print report for auto correlation counter.
        """
        print('Name: ' + self.name)
        for i in range(0, self.max_lag + 1):
            print('Lag = ' + str(i) + '; covariance = ' + str(self.get_auto_cov(i)) + '; correlation = ' + str(
                self.get_auto_cor(i)))
