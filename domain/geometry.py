import random
from typing import List, Union

from domain.areaofinterest import AreaOfInterest
from domain.process import Process
from domain.sensors import Sensor
import matplotlib.pyplot as plt
import numpy as np
from domain.utils import Place


class Geometry:
    def __init__(self, process: Process, sensors: List[Sensor], aoi: AreaOfInterest):
        self.process = process
        self.sensors = sensors
        self.aoi = aoi

    def draw(self):
        grid_size = 21  # fixed size for draw simplicity
        half_grid = (grid_size - 1) // 2  # This will help place (0,0) in the center

        def convert_to_grid_coords(x, y):
            # Shift the coordinates to place (0,0) in the center of the grid
            grid_x = int(x + half_grid)
            grid_y = int(y + half_grid)
            return grid_x, grid_y

        # Create a grid and set all to white initially
        grid = np.ones((grid_size, grid_size, 3))  # NxN pixels with RGB channels

        # Set Area of Interest to green
        for aoi in self.aoi:
            grid_x_aoi, grid_y_aoi = convert_to_grid_coords(aoi.x, aoi.y)
            grid[grid_size - grid_y_aoi - 1, grid_x_aoi] = [0, 1, 0]  # RGB for green

        # Set Process to red
        grid_x_process, grid_y_process = convert_to_grid_coords(self.process.place.x, self.process.place.y)
        grid[grid_size - grid_y_process - 1, grid_x_process] = [1, 0, 0]  # RGB for red

        # Set Sensors to grey
        for s in self.sensors:
            grid_x_sensor, grid_y_sensor = convert_to_grid_coords(s.place.x, s.place.y)
            grid[grid_size - grid_y_sensor - 1, grid_x_sensor] = [0, 0, 1]  # RGB for blue

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

    @staticmethod
    def generate_random_geometry(processType: Process, num_sensors, num_poi: Union[int, None] = None,
                                 poi: Union[List[Place], None] = None):
        sensors_place_range = np.linspace(-5, 5)

        p: Process = processType

        sensors = [Sensor(
            Place(random.choice(sensors_place_range), random.choice(sensors_place_range)),
            None
        ) for _ in range(num_sensors)]
        if poi is None:
            a: AreaOfInterest = AreaOfInterest([
                Place(random.choice(sensors_place_range), random.choice(sensors_place_range))
                for _ in range(num_poi)
            ])
        else:
            a: AreaOfInterest = AreaOfInterest(poi)

        return Geometry(process=p, sensors=sensors, aoi=a)
