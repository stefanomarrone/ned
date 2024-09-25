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
from typing import Union, List

import matplotlib.pyplot as plt
import numpy as np

from AoI import AreaOfInterest
from process import Process, SpikeProcess
from sensors import Sensor
from utils import ProbabilisticCharacterization, Place


class Geometry:
    def __init__(self, process: Process, sensors: List[Sensor], aoi: AreaOfInterest):
        self.process = process
        self.sensors = sensors
        self.aoi = aoi

    def draw_geometry(self):
        grid_size = 11  # fixed size for draw simplicity
        half_grid = (grid_size - 1) // 2  # This will help place (0,0) in the center

        def convert_to_grid_coords(x, y):
            # Shift the coordinates to place (0,0) in the center of the grid
            grid_x = int(x + half_grid)
            grid_y = int(y + half_grid)
            return grid_x, grid_y

        # Create a grid and set all to white initially
        grid = np.ones((grid_size, grid_size, 3))  # NxN pixels with RGB channels

        # Set Area of Interest to green
        for aoi in self.aoi.places:
            grid_x_aoi, grid_y_aoi = convert_to_grid_coords(aoi.x, aoi.y)
            grid[grid_size - grid_y_aoi - 1, grid_x_aoi] = [0, 1, 0]  # RGB for green

        # Set Process to red
        grid_x_process, grid_y_process = convert_to_grid_coords(self.process.place.x, self.process.place.y)
        grid[grid_size - grid_y_process - 1, grid_x_process] = [1, 0, 0]  # RGB for red

        # Set Sensors to grey
        for s in self.sensors:
            grid_x_sensor, grid_y_sensor = convert_to_grid_coords(s.place.x, s.place.y)
            grid[grid_size - grid_y_sensor - 1, grid_x_sensor] = [0.5, 0.5, 0.5]  # RGB for grey

        # Plot the grid
        plt.imshow(grid, extent=(-half_grid, half_grid, -half_grid, half_grid))
        plt.grid(True)

        # Add x and y axis labels
        plt.xlabel("x")
        plt.ylabel("y")

        # Show x and y ticks at regular intervals
        plt.xticks(np.arange(-half_grid, half_grid + 1, 1))
        plt.yticks(np.arange(-half_grid, half_grid + 1, 1))

        plt.title('Geometry Map')
        plt.show()


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
    return psuccess * (((dpaoi / dps) ** 2) * (1 / (sigma ** 2))) * measure


def temporal_expected_value(psuccess, dpaoi, dps, sigma, measure, decay=0.5):
    tev = 0
    for i in range(len(measure)):
        tev = tev + np.exp(-decay * (len(measure) - i)) * expected_value(psuccess, dpaoi, dps, sigma, measure[i])
    return tev


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


def run_simulation(geometry: Geometry, num_steps):
    process = []

    sensors = geometry.sensors
    aoi_places = geometry.aoi.places

    measures = {idx: [] for idx in range(len(sensors))}
    aois = {idx: [] for idx in range(len(aoi_places))}
    reconstructions = {idx: [] for idx in range(len(aoi_places))}

    for i in range(num_steps):
        v = geometry.process.generate()
        process.append(v)
        for idx, s in enumerate(sensors):
            measures[idx].append(
                transport_formula(v, s.probabilistic_characterization, geometry.process.place, s.place))
        for idx, place in enumerate(aoi_places):
            aois[idx].append(transport_formula(v, None, geometry.process.place, place))
            reconstructions[idx].append(expected_radiations(list(measures.values()), geometry, place, temporal=True))
    return process, measures, aois, reconstructions


if __name__ == '__main__':
    p: Process = SpikeProcess(ProbabilisticCharacterization(0, 0.02), 100, spike_rate=0.07,
                              spike_range=np.linspace(0, 70))
    # RandomWalkProcess(ProbabilisticCharacterization(2, 5), 10000, drift=0)
    s1: Sensor = Sensor(Place(1, 2), ProbabilisticCharacterization(0, 0.8))  # Best Places for Assessment
    s2: Sensor = Sensor(Place(1, -2), ProbabilisticCharacterization(0, 0.9))  # Best Places for Assessment
    s3: Sensor = Sensor(Place(-3, 0), ProbabilisticCharacterization(0, 0.9))  # Best Places for Assessment
    a: AreaOfInterest = AreaOfInterest([Place(5, 0), Place(2, 3)])

    geometry = Geometry(p, [s1, s2, s3], a)
    geometry.draw_geometry()

    # custom threshold for activation
    threshold = 130
    # ps = [p.generate() for _ in range(100)]
    # plt.figure(figsize=(20, 6))
    # plt.plot(ps)
    # plt.show()
    # generating process for 100 values and reading data
    process, measures, aois, recs = run_simulation(geometry, 20)
    plt.figure(figsize=(20, 6))
    plt.plot(process)
    plt.title('process')
    plt.show()

    num_measures = len(measures)
    print(num_measures)
    fig, axs = plt.subplots(num_measures, 1, figsize=(20, 6))
    for i in range(num_measures):
        try:
            axs[i].plot(measures[i])
            axs[i].set_title(f'sensor {i}')
        except TypeError as e:
            axs.plot(measures)
            axs.set_title('sensor')
    plt.show()

    num_aoi = len(aois)  # num recs and num aoi is the same because for each aoi i have a reconstruction
    fig, axs = plt.subplots(num_aoi, 2, figsize=(20, 6))
    for i in range(num_aoi):
        try:
            axs[i, 0].plot(aois[i])
            axs[i, 0].set_title(f'Point Of Interest {i}')
            axs[i, 1].plot(recs[i])
            axs[i, 1].set_title(f'Reconstruction Point Of Interest {i}')
        except Exception as e:
            axs[0].plot(aois[0])
            axs[0].set_title('Point Of Interest')
            axs[1].plot(recs[0])
            axs[1].set_title('Reconstruction Point Of Interest')
    plt.show()
