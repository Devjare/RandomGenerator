import numpy
from Distribution import Distribution
import math


class ExponentialDistribution(Distribution):
    def __init__(self, parameters):
        self.a = parameters['a']

    def get_probability(self, x, acc):
        if acc:
            return 1 - math.exp(-1 * x/self.a)
        else:
            return (1/self.a) * math.exp(-1*x/self.a)


    def get_sample(self, n):
        sample = []
        for i in range(n):
            u = numpy.random.uniform(0, 1, 1)[0]
            p = math.log(1 - u) / (-self.a)
            sample.append(p)
        return sample