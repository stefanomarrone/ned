import sys
from random import uniform
from typing import List

import matplotlib.pyplot as plt
import numpy as np

from domain.areaofinterest import AreaOfInterest
from domain.geometry import Geometry
from domain.process import Process, SpikeProcess
from domain.sensors import Sensor
from domain.utils import ProbabilisticCharacterization, Place, transport_formula, generate_table
from utils.configuration import Configuration


def run_simulation(geometry: Geometry, num_steps, vals=None):
    process = []
    sensors = geometry.sensors
    aoi_places = geometry.aoi.places

    measures = {idx: [] for idx in range(len(sensors))}
    aois = {idx: [] for idx in range(len(aoi_places))}
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
    return process, measures, aois


def poi_thr(val, d):
    return val / d


def main_run():
    process: Process = SpikeProcess(ProbabilisticCharacterization(0, 0.02), 100, spike_rate=0.07,
                                    spike_range=np.linspace(0, 70))
    poi: List[Place] = [Place(5, 0)]  # , Place(-5, 0), Place(0, 5), Place(0, -5)]
    sensors: List[Sensor] = [Sensor(Place(1, 2), None, psuccess=0.8), Sensor(Place(1, -2), None, psuccess=0.8)]
    geometry = Geometry(process, sensors, AreaOfInterest(places=poi))
    # geometry = Geometry.generate_random_geometry(process, num_sensors=3, poi=poi)
    geometry.draw_geometry()
    for idx, _ in enumerate(geometry.sensors):
        geometry.sensors[idx].probabilistic_characterization = ProbabilisticCharacterization(0, uniform(0.05, 1.2))
    process, measures, aois = run_simulation(geometry=geometry, num_steps=100)
    # print results
    plt.figure(figsize=(20, 6))
    plt.plot(process)
    plt.title('process')
    plt.show()
    num_measures = len(measures)
    fig, axs = plt.subplots(num_measures, 1, figsize=(20, 6))
    thr_measures = []
    thr_y = []
    for i in range(num_measures):
        thr = uniform(15, 25)  # random
        thr_y.append(thr)
        thr_mes = [0 if v < thr else 1 for v in measures[i]]
        thr_measures.append(thr_mes)
        try:
            axs[i].plot(measures[i])
            axs[i].plot(range(len(measures[i])), [thr] * len(measures[i]))
            axs[i].set_title(f'sensor {i}')
        except TypeError as e:
            axs.plot(measures)
            axs.plot(range(len(measures[0])), [thr] * len(measures[0]))
            axs.set_title('sensor')
    plt.show()
    num_aoi = len(aois)  # num recs and num aoi is the same because for each aoi i have a reconstruction
    fig, axs = plt.subplots(num_aoi, 1, figsize=(20, 6))
    # setting thresholds for AoI and sensors
    thr_aois = []
    for i in range(num_aoi):
        # a random number i set just for the sake of proving the correctness of the code: 150 / d(p,poi)
        thr = poi_thr(150, ((geometry.process.place.x - geometry.aoi.places[i].x) ** 2 + (
                geometry.process.place.y - geometry.aoi.places[i].y) ** 2))
        thr_aoi = [0 if v < thr else 1 for v in aois[i]]
        thr_aois.append(thr_aoi)
        try:
            axs[i].plot(aois[i])
            axs[i].plot(range(len(aois[i])), [thr] * len(aois[i]))
            axs[i].set_title(f'Point Of Interest {i}')
        except Exception as e:
            axs.plot(aois[0])
            axs.plot(range(len(aois[0])), [thr] * len(aois[0]))
            axs.set_title('Point Of Interest')
    plt.show()
    # plots for the paper
    fig, axs = plt.subplots(2, 2, figsize=(10, 8))
    # Plot ps on the first subplot
    axs[0, 0].plot(process)
    axs[0, 0].set_title('process')
    # Plot s1s on the second subplot
    axs[0, 1].plot(measures[0])
    axs[0, 1].plot(range(len(measures[0])), [thr_y[0]] * len(measures[0]))
    axs[0, 1].set_title('sensor 1')
    # Plot s2s on the third subplot
    axs[1, 0].plot(measures[1])
    axs[1, 0].plot(range(len(measures[1])), [thr_y[1]] * len(measures[1]))
    axs[1, 0].set_title('sensor 2')
    # Plot ass on the fourth subplot
    axs[1, 1].plot(aois[0])
    axs[1, 1].plot(range(len(aois[i])), [thr] * len(aois[i]))
    axs[1, 1].set_title('Area of Interest')
    # Add some padding between subplots
    plt.tight_layout()
    # Display the plots
    plt.show()
    print(generate_table(thr_measures, thr_aois))


if __name__ == '__main__':
    configuration_filename = sys.argv[1]
    config = Configuration(configuration_filename)
    main_run()
