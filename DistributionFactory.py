from BinomialDistribution import BinomialDistribution
from ExponentialDistribution import ExponentialDistribution
from NegativeBinomialDistribution import NegativeBinomialDistribution
from NormalDistribution import NormalDistribution
from PoissonDistribution import PoissonDistribution


class DistributionFactory:
    def __init__(self):
        pass

    @staticmethod
    def get_distribution(name, args):
        if name == 'binomial':
            return BinomialDistribution(args)
        elif name == 'negativebinomial':
            return NegativeBinomialDistribution(args)
        elif name == 'normal':
            return NormalDistribution(args)
        elif name == 'exponential':
            return ExponentialDistribution(args)
        elif name == 'poisson':
            return PoissonDistribution(args)
