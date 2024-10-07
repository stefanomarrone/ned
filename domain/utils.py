from typing import Union

import numpy as np


class Place:
    def __init__(self, x, y):
        # distance in meters from the origin
        self.x = x
        self.y = y

class SafetyMethod:
    pass

class Asset(Place):
    def __init__(self, x, y, th, sm: Union[SafetyMethod, None] = None):
        super().__init__(x,y)
        self.threshold = th
        self.safety_method = sm
    def getThreshold(self):
        return self.threshold

class ProbabilisticCharacterization:
    def __init__(self, mu, sigma):
        self.mu = mu
        self.sigma = sigma





def transport_formula(p_val, probabilistic_characterization: Union[ProbabilisticCharacterization, None], p_place: Place,
                      v_place: Place):
    val = p_val / ((p_place.x - v_place.x) ** 2 + (p_place.y - v_place.y) ** 2)
    if probabilistic_characterization is not None:
        e = np.random.normal(probabilistic_characterization.mu, probabilistic_characterization.sigma)
        val = val + e
    return val


