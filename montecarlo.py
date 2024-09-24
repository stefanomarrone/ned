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


    21/09/2024  michele.digiovanni@unicampania.it
"""
from random import random, choice
from typing import List, Union

import numpy as np
import matplotlib.pyplot as plt

from AoI import AreaOfInterest
from process import Process, SpikeProcess
from sensors import Sensor
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


# @TODO: how can i compute the threshold for the sensor? It can't be adjusted only by comparing f(p,si) < threshold/d(p,si)
#       otherwise it would oly be scaled but will not take into consideration that a very distant sensor can provide
#       a very bad insight

if __name__ == '__main__':
    p: Process = SpikeProcess(ProbabilisticCharacterization(0, 0.02), 100, spike_rate=0.07, spike_range=np.linspace(0,
                                                                                                                    70))
    # RandomWalkProcess(ProbabilisticCharacterization(2, 5), 10000, drift=0)
    s1: Sensor = Sensor(Place(1, 2), ProbabilisticCharacterization(0, 0.3))
    s2: Sensor = Sensor(Place(1, -2), ProbabilisticCharacterization(0, 0.05))
    a: AreaOfInterest = AreaOfInterest([Place(5, 0)])

    ps = []
    s1s = []
    s2s = []
    ass = []
    alerts = []

    # custom threshold for activation
    threshold = 130
    # ps = [p.generate() for _ in range(100)]
    # plt.figure(figsize=(20, 6))
    # plt.plot(ps)
    # plt.show()
    # generating process for 100 values and reading data
    for i in range(100):
        v = p.generate()
        ps.append(v)
        s1s.append(transport_formula(v, s1.probabilistic_characterization, p.place, s1.place))
        s2s.append(transport_formula(v, s2.probabilistic_characterization, p.place, s2.place))
        ass.append(transport_formula(v, None, p.place, a.places[0]))
        if v > threshold:
            alerts.append(1)
        else:
            alerts.append(0)

    fig, axs = plt.subplots(2, 2, figsize=(10, 8))

    # Plot ps on the first subplot
    axs[0, 0].plot(ps)
    axs[0, 0].set_title('ps')

    # Plot s1s on the second subplot
    axs[0, 1].plot(s1s)
    axs[0, 1].set_title('s1s')

    # Plot s2s on the third subplot
    axs[1, 0].plot(s2s)
    axs[1, 0].set_title('s2s')

    # Plot ass on the fourth subplot
    axs[1, 1].plot(ass)
    axs[1, 1].set_title('ass')

    # Add some padding between subplots
    plt.tight_layout()

    # Display the plots
    plt.show()

    plt.figure(figsize=(20, 6))
    plt.plot(alerts)
    plt.show()
