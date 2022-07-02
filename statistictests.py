import math

import numpy as np
from scipy.stats import chi2, norm, chisquare


def pdf_gaussian(x, mean, var):
    return (1 / np.sqrt(2 * np.pi * var)) * np.exp(-0.5 * np.square(x - mean) / var)


class ChiSquare(object):

    def __init__(self, emp_x, emp_n, name="default"):
        """
        Initialize chi square test with observations and their frequency.
        :param emp_x: observation values (bins)
        :param emp_n: frequency
        :param name: name for better distinction of tests
        """
        if len(emp_x) - 1 == len(emp_n):
            self.name = name
            self.emp_x = list(emp_x)
            self.emp_n = list(emp_n)
        else:
            raise ValueError("Wrong array lengths. emp_x must have k+1 values representing the bins' borders."
                             "emp_n with k values represent the frequencies of each bin")

    def test_distribution(self, alpha, mean, var):
        """
        Test, if the observations fit into a given distribution.
        :param alpha: significance of test
        :param mean: mean value of the gaussian distribution
        :param var: variance of the gaussian distribution
        """

        n = sum(self.emp_n)
        cdf_values = norm.cdf(np.array(self.emp_x), loc=mean, scale=np.sqrt(var))
        expected_freq = []
        for j in range(len(cdf_values) - 1):
            expected_freq.append(cdf_values[j + 1] - cdf_values[j])
        expected_freq = list(np.array(expected_freq) * n)
        # assert sum(expected_freq)==n

        k = 0
        head_freq = 0
        while head_freq < 5:
            head_freq += expected_freq[k]
            k += 1

        head_freq = 0
        head_obs = 0
        for _ in range(k):
            head_freq += expected_freq[_]
            head_obs += self.emp_n[_]

        for _ in range(k - 1):
            expected_freq.pop(0)
            self.emp_n.pop(0)

        expected_freq[0] = head_freq
        self.emp_n[0] = head_obs

        tail_freq = 0
        k = len(expected_freq) - 1
        while tail_freq < 5:
            tail_freq += expected_freq[k]
            k -= 1

        tail_freq = 0
        tail_obs = 0
        for _ in range(k + 1, len(expected_freq) - 1):
            tail_freq += expected_freq[_]
            tail_obs += self.emp_n[_]

        for _ in range(k + 1, len(expected_freq) - 1):
            expected_freq.pop()
            self.emp_n.pop()

        expected_freq[len(expected_freq) - 1] = tail_freq
        self.emp_n[len(self.emp_n) - 1] = tail_obs

        print(f'O_i = {self.emp_n}')
        print(f'E_i = {expected_freq}')

        df = len(self.emp_n) - 2 - 1
        # find Chi-Square value from table
        chi_square = chi2.ppf(1 - alpha, df=df)

        chi_hat = 0
        for obs, expect in zip(self.emp_n, expected_freq):
            chi_hat += ((obs - expect) ** 2) / expect

        return chi_hat, chi_square
