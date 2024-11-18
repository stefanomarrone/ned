import os
import random
from typing import List, Union, Optional

from domain.areaofinterest import AreaOfInterest
from domain.process import Process
from domain.sensors import Sensor
import matplotlib.pyplot as plt
import matplotlib.patches as patches

import numpy as np
from domain.utils import Place


class Geometry:
    def __init__(self, process: Process, sensors: List[Sensor], aoi: AreaOfInterest):
        self.process = process
        self.sensors = sensors
        self.aoi = aoi

    def draw(self, out_folder: Optional = None):
        grid_size = 11  # fixed size for draw simplicity
        half_grid = (grid_size - 1) // 2  # This will help place (0,0) in the center

        def convert_to_grid_coords(x, y):
            # Shift the coordinates to place (0,0) in the center of the grid
            grid_x = x + half_grid
            grid_y = y + half_grid
            return grid_x, grid_y

        fig, ax = plt.subplots(figsize=(8, 8))
        # Plot grid background
        ax.set_xlim(-half_grid, half_grid)
        ax.set_ylim(-half_grid, half_grid)
        ax.set_aspect('equal')
        ax.set_xticks(np.arange(-half_grid, half_grid + 1, 1))
        ax.set_yticks(np.arange(-half_grid, half_grid + 1, 1))
        ax.grid(True)
        ax.set_xlabel("x")
        ax.set_ylabel("y")
        ax.set_title("Geometry Map")

        sensor_patch = patches.Circle((0, 0), radius=0.4, color="blue", label="Sensors: Circles")
        aoi_patch = patches.RegularPolygon((0, 0), numVertices=3, radius=0.4, color="green",
                                           label="AoI: Triangle")
        process_patch = patches.Rectangle((0, 0), width=0.8, height=0.8, color="red", label="Process: Square")

        # Draw Area of Interest as green triangles
        for aoi in self.aoi:
            grid_x_aoi, grid_y_aoi = convert_to_grid_coords(aoi.x, aoi.y)
            triangle = patches.RegularPolygon(
                (grid_x_aoi - half_grid, grid_y_aoi - half_grid),  # position
                numVertices=3,  # triangle
                radius=0.5,  # size
                orientation=0,  # pointing up
                color="green"
            )
            ax.add_patch(triangle)

        # Draw Process as red square
        grid_x_process, grid_y_process = convert_to_grid_coords(self.process.place.x, self.process.place.y)
        square = patches.Rectangle(
            (grid_x_process - half_grid - 0.4, grid_y_process - half_grid - 0.4),
            0.8, 0.8, color="red"
        )
        ax.add_patch(square)

        # Draw Sensors as blue circles
        for s in self.sensors:
            grid_x_sensor, grid_y_sensor = convert_to_grid_coords(s.place.x, s.place.y)
            circle = patches.Circle(
                (grid_x_sensor - half_grid, grid_y_sensor - half_grid),
                radius=0.4, color="blue"
            )
            ax.add_patch(circle)
        ax.legend(handles=[sensor_patch, aoi_patch, process_patch], loc="upper right", title="Legend")

        # Save or show the figure
        if out_folder is not None:
            path = f'{os.getcwd()}/{out_folder}'
            if not os.path.exists(path):
                os.mkdir(path)
            plt.savefig(f"{out_folder}/geometry.pdf", format="pdf", bbox_inches="tight")
        else:
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
