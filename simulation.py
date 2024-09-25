"""
    Monte Carlo simulation for probability table generation.

    Given a Process P, characterized by a function P(t) placed in (x,y) = (0,0);
    A set of sensors [S1,S2,...,SN], characterized by an error of sensing N(mu,sigma), placed in (xi,yi);
    An area of interest placed in (xA,yA);
    And transport mechanism f(P(t),Si) = P(t)*(1/d(P,Si)^2 )+Error(mu,sigma,t), where d(P,Si) is the euclidean distance
    between the Process and the Sensor;
    This code aims to compute the relationship between the Process, the sensed value from a sensor and the radiation
    rate in the area A.

    ------------------------------------------------------------------------------------
    | t         |       P       |   S1        | S2        | ... | Sn       | A          |
    ------------------------------------------------------------------------------------
    |   t0      |       p0      |   f(p0,s1)  | f(p0,s2)  | ... | f(p0,sn) | p0/d(P,A)  |

    Hypothesizing an unknown process p(t), it is possible to use the sensors' measurements to compute the Expected
    Value of the radiations at the safe area.
    E[SafeArea(t)] = sum( Psuccess_i * alpha_i *w_i * M_i)
    Where: Psuccess_i is the probability of a correct measurement of the i-th sensor, that depends on the scheduling
    (activity time), and the battery (stress factor); M_i(t) is the i-th sensor's measure;
    And alpha_i is a scaling factor that takes into account the distance between the process and the safe area, the
    distance between the process and the sensor and, finally, a weight w_i that penalises the sensors with a highest
    variance, so alpha_i*w_i = (d(p,A)/d(p,si)^2 * 1/sigma_i^2

    Finally, after the computation of the EV, it is possible to check it with the "real" (simulated) p(t) in the Safe
    Area in order to understand how good the estimate was.

    21/09/2024  michele.digiovanni@unicampania.it
"""
from typing import Union

import numpy as np

from geometry import Geometry
from utils import ProbabilisticCharacterization, Place


def transport_formula(p_val, probabilistic_characterization: Union[ProbabilisticCharacterization, None], p_place: Place,
                      v_place: Place):
    val = p_val / ((p_place.x - v_place.x) ** 2 + (p_place.y - v_place.y) ** 2)
    if probabilistic_characterization is not None:
        e = np.random.normal(probabilistic_characterization.mu, probabilistic_characterization.sigma)
        val = val + e
    return val


# @TODO: full Monte Carlo implementation and table creation
def generate_table():
    pass


"""
    measures should have N lists, where N is the number of sensors from geometry
    
    measures = [
        [1,2,3...],
        [3,5,6,..],
        ...,
        [4,5,6,...]
    ]
    
"""


def expected_value(psuccess, dpaoi, dps, sigma, measure):
    return psuccess * (((dpaoi / (dps + dpaoi)) ** 2) * (1 / (sigma ** 2))) * measure


def temporal_expected_value(psuccess, dpaoi, dps, sigma, measure, decay=100):
    # tev = 0
    # for i in range(len(measure)):
    #    tev = tev + np.exp(-decay * ((len(measure)-1) - i)) * expected_value(psuccess, dpaoi, dps, sigma, measure[i])
    # Fake temporal decay
    return expected_value(psuccess, dpaoi, dps, sigma, measure[-1])


def expected_radiations(measures, geometry: Geometry, poi: Place, temporal=False):
    # An Area Of Interest is composed of several Points Of Interest!!!
    num_sensors = len(geometry.sensors)
    num_ev = 0
    den_ev = 0
    dpaoi = np.sqrt((geometry.process.place.x - poi.x) ** 2 + (
            geometry.process.place.y - poi.y) ** 2)
    f = {True: temporal_expected_value, False: expected_value}

    for i in range(num_sensors):
        dps = np.sqrt((geometry.process.place.x - geometry.sensors[i].place.x) ** 2 + (
                geometry.process.place.y - geometry.sensors[i].place.y) ** 2)
        if temporal:
            if isinstance(measures[i], list) is False:
                raise ValueError("In temporal mode, each measure should be a list of length N (number of time steps).")

        else:
            if isinstance(measures[i], (int, float)) is False:
                raise ValueError("In non-temporal mode, each measure should be a scalar value.")
        num_ev = num_ev + f[temporal](psuccess=geometry.sensors[i].psuccess, dpaoi=dpaoi, dps=dps,
                                      sigma=geometry.sensors[i].probabilistic_characterization.sigma,
                                      measure=measures[i])
        # normalization factor
        den_ev = den_ev + f[temporal](psuccess=geometry.sensors[i].psuccess, dpaoi=1, dps=1,
                                      sigma=geometry.sensors[i].probabilistic_characterization.sigma,
                                      measure=1 if not temporal else [1] * len(measures[i]))

    return (num_ev / den_ev) / (dpaoi ** 2)


def run_simulation(geometry: Geometry, num_steps, vals=None):
    process = []

    sensors = geometry.sensors
    aoi_places = geometry.aoi.places

    measures = {idx: [] for idx in range(len(sensors))}
    aois = {idx: [] for idx in range(len(aoi_places))}
    reconstructions = {idx: [] for idx in range(len(aoi_places))}
    if vals is not None:
        num_steps = len(vals)

    for i in range(num_steps):
        if vals is None:
            v = geometry.process.generate()
        else:
            v = vals[i]
        process.append(v)
        for idx, s in enumerate(sensors):
            measures[idx].append(
                transport_formula(v, s.probabilistic_characterization, geometry.process.place, s.place))
        for idx, place in enumerate(aoi_places):
            aois[idx].append(transport_formula(v, None, geometry.process.place, place))
            reconstructions[idx].append(expected_radiations(list(measures.values()), geometry, place, temporal=True))
    return process, measures, aois, reconstructions
