from matplotlib import pyplot as plt

class Results:

    def __init__(self, pprocess, ssensors, aassets, tthresholds):
        self.process = pprocess
        self.sensors = ssensors
        self.assets = aassets
        self.thresholds = tthresholds

    def __len__(self):
        return len(self.sensors.keys())

    def draw_process(self, output_folder):
        plt.figure(figsize=(20, 6))
        plt.plot(self.process)
        plt.title('process')
        plt.savefig(output_folder + "process.pdf", format="pdf", bbox_inches="tight")

    def draw_sensors(self, output_folder):
        num_measures = len(self.sensors.keys())
        fig, axs = plt.subplots(num_measures, 1, figsize=(20, 6))
        thr_y = []
        i = 0
        for sensor_name in self.sensors.keys():
            sensor = self.sensors[sensor_name]
            thr = self.thresholds[sensor_name]
            thr_y.append(thr)
            axs[i].plot(sensor)
            axs[i].plot(range(len(sensor)), [thr] * len(sensor))
            axs[i].set_title(sensor_name)
            i += 1
        plt.savefig(output_folder + "sensor.pdf", format="pdf", bbox_inches="tight")

    def draw_asset(self, output_folder):
        data = self.assets[0]
        fig, axs = plt.subplots(1, 1, figsize=(20, 6))
        thr = self.thresholds['asset']
        axs.plot(data)
        axs.plot(range(len(data)), [thr] * len(data))
        axs.set_title('asset')
        plt.savefig(output_folder + "asset.pdf", format="pdf", bbox_inches="tight")

    def draw(self, output_folder):
        self.draw_process(output_folder)
        self.draw_sensors(output_folder)
        self.draw_asset(output_folder)