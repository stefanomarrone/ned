from domain.process import Process, SpikeProcess, RandomWalkProcess
from domain.utils import ProbabilisticCharacterization
import numpy as np

class ProcessFactory:
    @staticmethod
    def generate(process_parameters):
        mu = process_parameters['mu']
        sigma = process_parameters['sigma']
        level = process_parameters['level']
        probabilistic = ProbabilisticCharacterization(mu, sigma)
        return probabilistic, level

class SpikeProcessFactory(ProcessFactory):
    @staticmethod
    def generate(process_parameters):
        probabilistic, level = ProcessFactory.generate(process_parameters)
        rate = process_parameters['rate']
        range = process_parameters['range']
        process = SpikeProcess(probabilistic, level, spike_rate=rate, spike_range = np.linspace(0, range))
        return process


class WalkProcessFactory(ProcessFactory):
    @staticmethod
    def generate(process_parameters):
        probabilistic, level = ProcessFactory.generate(process_parameters)
        drift = process_parameters['drift']
        process = RandomWalkProcess(probabilistic, level, drift=drift)
        return process


class ProcessFactoryRegistry:
    registry= {
        'spike': SpikeProcessFactory,
        'walk': WalkProcessFactory
    }

    def getFactory(kind):
        return ProcessFactoryRegistry.registry[kind]
