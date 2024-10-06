from typing import Union

import numpy as np
import pandas as pd


class Place:
    def __init__(self, x, y):
        # distance in meters from the origin
        self.x = x
        self.y = y

class Asset(Place):
    def __init__(self, x, y, th):
        super().__init__(x,y)
        self.threshold = th

    def getThreshold(self):
        return self.threshold

class ProbabilisticCharacterization:
    def __init__(self, mu, sigma):
        self.mu = mu
        self.sigma = sigma


class SafetyMethod:
    pass


def transport_formula(p_val, probabilistic_characterization: Union[ProbabilisticCharacterization, None], p_place: Place,
                      v_place: Place):
    val = p_val / ((p_place.x - v_place.x) ** 2 + (p_place.y - v_place.y) ** 2)
    if probabilistic_characterization is not None:
        e = np.random.normal(probabilistic_characterization.mu, probabilistic_characterization.sigma)
        val = val + e
    return val


