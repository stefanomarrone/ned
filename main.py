import random
from typing import List

import numpy as np

from geometry import Geometry
from process import Process, SpikeProcess
from utils import ProbabilisticCharacterization, Place

if __name__ == '__main__':
    process: Process = SpikeProcess(ProbabilisticCharacterization(0, 0.02), 100, spike_rate=0.07,
                                    spike_range=np.linspace(0, 70))
    poi: List[Place] = [Place(5, 0)]

    geometry = Geometry.generate_random_geometry(process, num_sensors=10, poi=poi)
    geometry.draw_geometry()

    for idx, _ in enumerate(geometry.sensors):
        geometry.sensors[idx].probabilistic_characterization = ProbabilisticCharacterization(0,
                                                                                             random.uniform(0.05, 0.9))
