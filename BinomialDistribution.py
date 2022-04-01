import numpy

from Distribution import Distribution
from math import comb


class BinomialDistribution(Distribution):
    def __init__(self, parameters):
        self.n = parameters['n']
        self.p = parameters['p']
        self.q = 1 - parameters['p']

    def get_probability(self, x, acc):
        if acc:
            p_acc = 0
            for i in range(x + 1):
                probability = comb(self.n, i) * (self.p ** i) * (self.q ** (self.n - i))
                p_acc = p_acc + probability
            return p_acc
        else:
            return comb(self.n, x) * (self.p ** x) * (self.q ** (self.n - x))

    def get_sample(self, n):
        sample = []
        for i in range(n):
            u = numpy.random.uniform(0, 1, 1)[0]
            print("U: ", u)
            k = 0
            p_aux = self.get_probability(k, True)
            while True:
                k += 1
                p_aux += self.get_probability(k, False)
                print("p_aux = ", p_aux)
                if p_aux > u:
                    break
            sample.append(k)
        return sample
