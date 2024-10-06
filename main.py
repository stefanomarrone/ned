import sys

from bayes.inference import Network
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
    table = results.get_detection_table()
    network = Network(results.get_sensor_names())
    network.build(table)
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