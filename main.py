from random import uniform
from typing import List

import numpy as np

from geometry import Geometry
from process import Process, SpikeProcess
from utils import ProbabilisticCharacterization, Place, transport_formula

import matplotlib.pyplot as plt


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


if __name__ == '__main__':
    process: Process = SpikeProcess(ProbabilisticCharacterization(0, 0.02), 100, spike_rate=0.07,
                                    spike_range=np.linspace(0, 70))
    poi: List[Place] = [Place(5, 0)]  # , Place(-5, 0), Place(0, 5), Place(0, -5)]

    geometry = Geometry.generate_random_geometry(process, num_sensors=3, poi=poi)
    geometry.draw_geometry()

    for idx, _ in enumerate(geometry.sensors):
        geometry.sensors[idx].probabilistic_characterization = ProbabilisticCharacterization(0, uniform(0.05, 0.9))

    process, measures, aois = run_simulation(geometry=geometry, num_steps=100)

    # print results

    plt.figure(figsize=(20, 6))
    plt.plot(process)
    plt.title('process')
    plt.show()

    num_measures = len(measures)
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
    fig, axs = plt.subplots(num_aoi, 1, figsize=(20, 6))
    for i in range(num_aoi):
        try:
            axs[i].plot(aois[i])
            axs[i].set_title(f'Point Of Interest {i}')
        except Exception as e:
            axs.plot(aois[0])
            axs.set_title('Point Of Interest')
    plt.show()
