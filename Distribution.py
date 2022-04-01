from abc import abstractmethod, ABC


class Distribution(ABC):
    def __init__(self, parameters):
        self.parameters = parameters

    @abstractmethod
    def get_probability(self, x, acc):
        pass

    @abstractmethod
    def get_sample(n):
        pass