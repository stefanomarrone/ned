from utils import Place, ProbabilisticCharacterization


class Sensor:
    def __init__(self, place: Place, probabilistic_characterization: ProbabilisticCharacterization):
        self.place: Place = place
        # a good sensor can have a pc like mu = 0, std = 2
        self.probabilistic_characterization = probabilistic_characterization
