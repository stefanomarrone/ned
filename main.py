import sys
from bayes.bayesian import Network
from domain.geometry import Geometry
from domain.results import Results
from domain.sensors import Sensor
from domain.utils import transport_formula, Asset
from domain.factory import ProcessFactoryRegistry
from gspn_model.engine import Engine
from gspn_model.modelfactory import PlainModelFactory
from utils.configuration import Configuration


def run_simulation(geometry: Geometry, num_steps):
    process = []
    sensor_names = list(map(lambda s: s.getName(), geometry.sensors))
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
    thresholds['asset'] = aoi_places[0].getThreshold()  # todo: extends in case of multiple asset
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
    # @TODO: refactor Geometry's last parameter in AssetsOfInterest
    geometry = Geometry(process, sensors, [asset])
    return geometry


def make_global_parameters(analysis, activation_rate, deactivation_rate, config):
    retval = {'process':
                  {'activation_rate': activation_rate,
                   'deactivation_rate': deactivation_rate}}
    retval['sensors'] = dict()
    for sensor_name in analysis:
        retval['sensors'][sensor_name] = {'detection_probability': analysis[sensor_name]}
    retval['scheduler'] = {'on_rate': config.get('on_rate'),
                           'off_rate': config.get('off_rate'),
                           'kind': config.get('scheduler')}
    return retval


def core(configuration_filename, draw_flag):
    safety_measure = 0
    sustainability_measure = 0
    config = Configuration(configuration_filename)
    geometry = build(config)
    number_of_steps = config.get('simulation_steps')
    error = True
    while error:
        results = run_simulation(geometry=geometry, num_steps=number_of_steps)
        table = results.get_detection_table()
        network = Network(results.get_sensor_names())
        network.build(table)
        analysis = network.analysis()
        error = not bool(analysis)
        if not error:
            activation_rate, deactivation_rate = results.get_process_activation_deactivation_rates()
            error = activation_rate == 0 or deactivation_rate == 0
            global_parameters = make_global_parameters(analysis, activation_rate, deactivation_rate, config)
            gspn_repo = config.get('greatspn_repos')
            engine = PlainModelFactory.generate(global_parameters, gspn_repo)
            engine.execute()
            safety_measure = engine.safety()
            sustainability_measure = engine.sustainability()
            # gspn_naive_handle.one_sensor_analysis()
    if draw_flag:
        out_folder = config.get('outfolder')
        geometry.draw(out_folder)
        results.draw(out_folder)
    return safety_measure, sustainability_measure


if __name__ == '__main__':
    if len(sys.argv) >= 2:
        configuration_filename = sys.argv[1]
        drawing_flag = (len(sys.argv) > 2) and (sys.argv.__contains__('--draw'))
        core(configuration_filename, drawing_flag)
