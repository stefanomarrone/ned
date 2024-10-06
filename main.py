import sys
from domain.geometry import Geometry
from domain.results import Results
from domain.sensors import Sensor
from domain.utils import transport_formula, Asset
from domain.factory import ProcessFactoryRegistry
from utils.configuration import Configuration

def run_simulation(geometry: Geometry, num_steps):
    process = []
    sensor_names = list(map(lambda s: s.getName(),geometry.sensors))
    aoi_places = geometry.aoi
    measures = {name: [] for name in sensor_names}
    aois = {idx: [] for idx in range(len(aoi_places))}
    for i in range(num_steps):
        v = geometry.process.generate()
        process.append(v)
        for s in geometry.sensors:
            name = s.getName()
            data = transport_formula(v, s.probabilistic_characterization, geometry.process.place, s.place)
            measures[name].append(data)
        for idx, place in enumerate(aoi_places):
            aois[idx].append(transport_formula(v, None, geometry.process.place, place))
    # Threshold
    thresholds = dict()
    for s in geometry.sensors:
        thresholds[s.getName()] = s.getThreshold()
    thresholds['asset'] = aoi_places[0].getThreshold()    # todo: extends in case of multiple asset
    results = Results(process, measures, aois, thresholds)
    return results

def draw_plots(results):
    pass
'''
    # print results
    plt.figure(figsize=(20, 6))
    plt.plot(process)
    plt.title('process')
    plt.show()
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

'''

def build(configuration):
    # Process setting
    process_info = configuration.get('process')
    process_kind = process_info['kind']
    process_factory = ProcessFactoryRegistry.getFactory(process_kind)
    process = process_factory.generate(process_info)
    # Asset setting
    asset_threshold = configuration.get('hazardlevel')
    asset_x, asset_y = configuration.get('asset')
    asset = Asset(asset_x, asset_y, asset_threshold)
    # Sensors setting
    sensors = configuration.get('sensors')
    sensors = list(map(lambda x: Sensor(x, configuration.get(x)), sensors))
    # geometry
    geometry = Geometry(process, sensors, [asset])
    return geometry

def core(configuration_filename, draw_flag):
    config = Configuration(configuration_filename)
    geometry = build(config)
    number_of_steps = config.get('simulation_steps')
    results = run_simulation(geometry=geometry, num_steps=number_of_steps)


    num_measures = len(results)
    if draw_flag:
        out_folder = config.get('outfolder')
        geometry.draw(out_folder)
        results.draw(out_folder)
    pass

if __name__ == '__main__':
    if len(sys.argv) >= 2:
        configuration_filename = sys.argv[1]
        drawing_flag = (len(sys.argv) > 2) and (sys.argv.__contains__('--draw'))
        core(configuration_filename, drawing_flag)