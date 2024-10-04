import matplotlib.pyplot as plt
import numpy as np

from domain.areaofinterest import AreaOfInterest
from domain.geometry import Geometry
from domain.process import Process, SpikeProcess
from domain.sensors import Sensor
from simulation import run_simulation, analyse_simulation
from domain.utils import ProbabilisticCharacterization, Place

if __name__ == '__main__':
    p: Process = SpikeProcess(ProbabilisticCharacterization(0, 0.02), 100, spike_rate=0.07,
                              spike_range=np.linspace(0, 70))
    # RandomWalkProcess(ProbabilisticCharacterization(2, 5), 10000, drift=0)
    s1: Sensor = Sensor(Place(1, 2), ProbabilisticCharacterization(0, 0.3))  # Best Places for Assessment
    s2: Sensor = Sensor(Place(1, -2), ProbabilisticCharacterization(0, 0.05))  # Best Places for Assessment
    # s3: Sensor = Sensor(Place(1,0), ProbabilisticCharacterization(0,0.1))
    a: AreaOfInterest = AreaOfInterest([Place(5, 0)])
    geometry = Geometry(p, [s1, s2], a)  # Geometry(p, [s1,s2,s3], a)
    geometry.draw_geometry()

    process, measures, aois, recs = run_simulation(geometry, 100)

    print(analyse_simulation(aois, recs))
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
