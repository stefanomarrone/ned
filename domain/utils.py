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


def generate_table(val_sensors, val_pois):
    t = []
    title = [f'sensor {idx}' for idx, _ in enumerate(val_sensors)]
    title.extend([f'Poi {idx}' for idx, _ in enumerate(val_pois)])
    num_sensors, num_pois = len(val_sensors), len(val_pois)
    num_vals = len(val_sensors[0])
    for j in range(num_vals):
        vec = [val_sensors[i][j] for i in range(num_sensors)]
        vec.extend([val_pois[i][j] for i in range(num_pois)])
        vec = np.array(vec)
        t.append(vec)
    t = np.array(t)
    table = pd.DataFrame(t)
    table.columns = title
    return table
