from typing import Union

from domain.utils import Place, ProbabilisticCharacterization


class Scheduler:
    def __init__(self, measurement_time, time_down):
        self.measurement_time = measurement_time


class Sensor:
    def __init__(self, name, parameters):
        x, y = parameters.get('position')
        threshold = parameters.get('threshold')
        mu = parameters.get('mu')
        sigma = parameters.get('sigma')
        self.place: Place = Place(x, y)
        self.probabilistic_characterization: Union[ProbabilisticCharacterization, None] = ProbabilisticCharacterization(mu, sigma)
        self.name = name
        self.threshold = threshold
        # For now we don't have a scheduler and battery class for the sensor,
        # so the probability of success  is given outside
