from matplotlib import pyplot as plt
import pandas as pd


class ActivationRateException(Exception):
    def __init__(self, message):
        # Call the base class constructor with the parameters it needs
        super().__init__(message)
        self.message = message


class Results:

    def __init__(self, pprocess, ssensors, aassets, tthresholds):
        self.process = pprocess
        self.sensors = ssensors
        self.assets = aassets
        self.thresholds = tthresholds

    def __len__(self):
        return len(self.sensors.keys())

    def number_of_samples(self):
        sensor_names = list(self.sensors.keys())
        key = sensor_names[0]
        data_sample = self.sensors[key]
        return len(data_sample)

    def get_sensor_names(self):
        return list(self.sensors.keys())

    def draw_process(self, output_folder):
        plt.figure(figsize=(20, 6))
        plt.plot(self.process)
        # plt.title('process')
        plt.xlabel("time (s)")
        plt.ylabel("Count Rate")
        plt.savefig(output_folder + "process.pdf", format="pdf", bbox_inches="tight")

    def draw_sensors(self, output_folder):
        num_measures = len(self.sensors.keys())
        fig, axs = plt.subplots(num_measures, 1, figsize=(20, 8))
        plt.subplots_adjust(hspace=0.3)
        i = 0
        for sensor_name in self.sensors.keys():
            sensor = self.sensors[sensor_name]
            thr = self.thresholds[sensor_name]
            try:
                axs[i].plot(sensor)
                axs[i].plot(range(len(sensor)), [thr] * len(sensor))
                axs[i].set_title(sensor_name)
                axs[i].set_xlabel("time (s)")
                axs[i].set_ylabel("Count Rate")

            except Exception as e:
                axs.plot(sensor)
                axs.plot(range(len(sensor)), [thr] * len(sensor))
                axs.set_title(sensor_name)
                axs.xlabel("time (s)")
                axs.ylabel("Count Rate")
            i += 1
        plt.savefig(output_folder + "sensor.pdf", format="pdf", bbox_inches="tight")

    def draw_asset(self, output_folder):
        data = self.assets[0]
        fig, axs = plt.subplots(1, 1, figsize=(20, 6))
        thr = self.thresholds['asset']
        axs.plot(data)
        axs.plot(range(len(data)), [thr] * len(data))
        # axs.set_title('asset')
        axs.set_xlabel("time (s)")
        axs.set_ylabel("Count Rate")
        plt.savefig(output_folder + "asset.pdf", format="pdf", bbox_inches="tight")

    def draw(self, output_folder):
        self.draw_process(output_folder)
        self.draw_sensors(output_folder)
        self.draw_asset(output_folder)

    # todo: it works just in case of one asset
    def get_detection_table(self):
        detection = dict(self.sensors)
        detection['asset'] = self.assets[0]
        for key in detection.keys():
            threshold = self.thresholds[key]
            detection[key] = list(map(lambda x: x >= threshold, detection[key]))
        table = pd.DataFrame(detection)
        return table

    def get_process_rate(self, from_value):
        table = dict(self.get_detection_table())
        data = list(table['asset'])
        indices = range(len(data))
        merged_list = tuple(zip(indices, data))
        intervals = []
        counter = 1
        while counter < len(data):
            old = merged_list[counter - 1]
            new = merged_list[counter]
            if new[1] != old[1]:
                intervals.append(counter)
            counter += 1
        if data[0] == from_value:
            intervals.insert(0, 0)
        if len(intervals) % 2 > 0:
            intervals = intervals[:-1]
        counter = 0
        differences = []
        while counter < len(intervals):
            differences.append(intervals[counter + 1] - intervals[counter])
            counter += 2
        return float(sum(differences)) / float(len(differences))

    def get_process_activation_deactivation_rates(self):
        activations = 0
        deactivations = 0
        try:
            activations = 1 / self.get_process_rate(False)
            deactivations = 1 / self.get_process_rate(True)
        except Exception as s:
            print(s)
            e = ActivationRateException(message='Activation or Deactivation rate is 0!!')
            raise e
        return activations, deactivations
