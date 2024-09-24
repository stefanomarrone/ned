from random import random, choice

import numpy as np

from utils import Place, ProbabilisticCharacterization


class Process:
    def __init__(self):
        # the Process is placed at the origin
        self.place: Place = Place(0, 0)

    # There are several ways to generate a process, maybe we can return a constant value + a noise
    # or something more complex. It depends on what we want to prove.
    def generate(self):
        pass


class RandomWalkProcess(Process):
    def __init__(self, probabilistic_characterization: ProbabilisticCharacterization, start_val, drift=10):
        super().__init__()
        self.probabilistic_characterization = probabilistic_characterization
        self.val = start_val
        self.drift = drift

    def generate(self):
        self.val = self.val + np.random.normal(self.probabilistic_characterization.mu,
                                               self.probabilistic_characterization.sigma) + self.drift
        return self.val


class SpikeProcess(Process):
    def __init__(self, probabilistic_characterization: ProbabilisticCharacterization, start_val, spike_rate,
                 spike_range):
        super().__init__()
        self.probabilistic_characterization = probabilistic_characterization
        self.val = start_val
        self.spike_rate = spike_rate
        self.spike_range = spike_range

    def generate(self):
        if random() > self.spike_rate:
            self.val = self.val + np.random.normal(self.probabilistic_characterization.mu,
                                                   self.probabilistic_characterization.sigma)
            return self.val
        else:
            return self.val + choice(self.spike_range)

    def __probabilistic_return(self):
        return choice(self.spike_range) if random() < self.spike_rate else 0
