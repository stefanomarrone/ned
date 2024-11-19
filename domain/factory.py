import csv
import os

from domain.process import Process, SpikeProcess, RandomWalkProcess, FileProcess
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
        process = SpikeProcess(probabilistic, level, spike_rate=rate, spike_range=np.linspace(0, range))
        return process


class WalkProcessFactory(ProcessFactory):
    @staticmethod
    def generate(process_parameters):
        probabilistic, level = ProcessFactory.generate(process_parameters)
        drift = process_parameters['drift']
        process = RandomWalkProcess(probabilistic, level, drift=drift)
        return process


class FileProcessFactory(ProcessFactory):
    @staticmethod
    def generate(process_parameters):
        file_path = process_parameters['filepath']
        file_name = process_parameters['filename']
        complete_path = f'{os.getcwd()}/{file_path}{file_name}'

        with open(complete_path, 'r') as file:
            reader = csv.reader(file)
            headers = next(reader, None)
            column = {}
            for h in headers:
                column[h] = []
            for row in reader:
                for h, v in zip(headers, row):
                    if h != 'Data' and h != 'Ora':
                        v = int(v)
                    column[h].append(v)
        return FileProcess(data=column['Coincidenze analizzate'])


class ProcessFactoryRegistry:
    registry = {
        'spike': SpikeProcessFactory,
        'walk': WalkProcessFactory,
        'file': FileProcessFactory
    }

    def getFactory(kind):
        return ProcessFactoryRegistry.registry[kind]
