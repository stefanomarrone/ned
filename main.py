import random
from typing import List

import numpy as np

from AoI import AreaOfInterest
from geometry import Geometry
from simulation import run_simulation
from process import Process, SpikeProcess
from sensors import Sensor
from utils import ProbabilisticCharacterization, Place
import matplotlib.pyplot as plt


def analyse_simulation(aois, recs):
    aois_rmse = []
    for i in range(len(aois)):
        aois_rmse.append(np.sqrt(np.mean((np.array(aois[i]) - np.array(recs[i])) ** 2)))
    return aois_rmse


def generate_random_geometry():
    num_sensors = 2
    sensors_place_range = np.linspace(-5, 5)
    # sensors_sigma_range = np.linspace(0, 1)

    p: Process = SpikeProcess(ProbabilisticCharacterization(0, 0.02), 100, spike_rate=0.07,
                              spike_range=np.linspace(0, 70))

    sensors = [Sensor(
        Place(random.choice(sensors_place_range), random.choice(sensors_place_range)),
        ProbabilisticCharacterization(0, 0.05)
    ) for _ in range(num_sensors)]

    a: AreaOfInterest = AreaOfInterest([Place(5, 0)])

    return p, sensors, a


def format_simulation(geometry: Geometry, sim_res):
    stringa = ''
    for i in range(len(geometry.sensors)):
        stringa += f'sensore {i} -- posizione ({geometry.sensors[i].place.x},{geometry.sensors[i].place.y}), '
    stringa += f' {sim_res}'
    print(stringa)


if __name__ == '__main__':
    sim_res = []
    geometries: List[Geometry] = []
    process: Process = SpikeProcess(ProbabilisticCharacterization(0, 0.02), 100, spike_rate=0.07,
                                    spike_range=np.linspace(0, 70))
    AoI: AreaOfInterest = AreaOfInterest([Place(5, 0)])
    num_steps = 300
    val_process = [process.generate() for i in range(num_steps)]
    all_measures = []
    all_aois = []
    all_recs = []

    plt.figure(figsize=(20, 6))
    plt.plot(val_process)
    plt.title('process')
    plt.show()

    for i in range(100000):
        _, sensors, _ = generate_random_geometry()
        geometry = Geometry(process, sensors, AoI)  # Geometry(p, [s1,s2,s3], a)
        geometries.append(geometry)
        # geometry.draw_geometry()
        try:
            _, measures, aois, recs = run_simulation(geometry, num_steps, vals=val_process)
            sim_res.append(analyse_simulation(aois, recs))
            all_measures.append(measures)
            all_aois.append(aois)
            all_recs.append(recs)
        except Exception as e:
            sim_res.append(100000)
            all_measures.append(None)
            all_aois.append(None)
            all_recs.append(None)
            print('aaaa\n')
        # format_simulation(geometry, sim_res)

    print(sim_res, len(sim_res))
    min_res = np.min(sim_res)
    min_pos = np.argmin(sim_res)
    # let's plot the min res configuration
    print(min_pos)
    print(format_simulation(geometries[min_pos], min_res))
    g: Geometry = geometries[min_pos]
    g.draw_geometry()
    num_measures = len(all_measures[min_pos])
    fig, axs = plt.subplots(num_measures, 1, figsize=(20, 6))
    for i in range(num_measures):
        try:
            axs[i].plot(all_measures[min_pos][i])
            axs[i].set_title(f'sensor {i}')
        except TypeError as e:
            axs.plot(all_measures[min_pos])
            axs.set_title('sensor')
    plt.show()

    num_aoi = len(all_aois[min_pos])  # num recs and num aoi is the same because for each aoi i have a reconstruction
    fig, axs = plt.subplots(num_aoi, 2, figsize=(20, 6))
    for i in range(num_aoi):
        try:
            axs[i, 0].plot(all_aois[min_pos][i])
            axs[i, 0].set_title(f'Point Of Interest {i}')
            axs[i, 1].plot(all_recs[min_pos][i])
            axs[i, 1].set_title(f'Reconstruction Point Of Interest {i}')
        except Exception as e:
            axs[0].plot(all_aois[min_pos][0])
            axs[0].set_title('Point Of Interest')
            axs[1].plot(all_recs[min_pos][0])
            axs[1].set_title('Reconstruction Point Of Interest')
    plt.show()
