from utils import Place, ProbabilisticCharacterization


class Scheduler:
    def __init__(self, measurement_time, time_down):
        self.measurement_time = measurement_time


class Sensor:
    def __init__(self, place: Place, probabilistic_characterization: ProbabilisticCharacterization,
                 battery_capacity=1220, psuccess=1):
        self.place: Place = place
        # a good sensor can have a pc like mu = 0, std = 2
        self.probabilistic_characterization = probabilistic_characterization
        self.battery_capacity = battery_capacity
        # For now we don't have a scheduler and battery class for the sensor,
        # so the probability of success  is given outside
        self.psuccess = psuccess
