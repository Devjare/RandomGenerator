import numpy
from Distribution import Distribution
from math import comb


class NegativeBinomialDistribution(Distribution):
    def __init__(self, parameters):
        self.r = parameters['r']
        self.p = parameters['p']
        self.q = 1 - parameters['p']

    def get_probability(self, n, acc):
        if n < self.r:
            return -1
        if acc:
            p_acc = 0
            for i in range(self.r, n + 1):
                k = i - self.r
                probability = comb(k + self.r - 1, k) * (self.q ** self.r) * (self.p ** k)
                p_acc += probability

            return p_acc
        else:
            k = n - self.r
            return comb(k + self.r - 1, k) * (self.q ** self.r) * (self.p ** k)

    def get_sample(self, n):
        sample = []
        print("######################### Binomial sampling! ################# ")
        for i in range(n):
            u = numpy.random.uniform(0, 1, 1)[0]
            k = self.r
            p_aux = self.get_probability(k, False)
            print("k: %d, p_aux: %f" % (k, p_aux))
            while True:
                k += 1
                p_aux += self.get_probability(k, False)
                print("k: %d, p_aux: %f" % (k, p_aux))
                if (p_aux > u):
                    break
            sample.append(k)
        return sample