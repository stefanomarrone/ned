from gspn_model.engine import Engine


# todo: move from static  method to instance methods


class ModelAbstractFactory:
    @staticmethod
    def generate(gspn_parameters, repository_folder):
        pass


class PlainModelFactory:

    @staticmethod
    def simple(db, labelOne, labelTwo):
        return db[labelOne][labelTwo]

    @staticmethod
    def indexed(db, group, index, feature):
        labels = list(db[group].keys())
        label = labels[index]
        return db[group][label][feature]

    configurations = {
        'one': {
            'EventStartRate': lambda conf: PlainModelFactory.simple(conf, 'process', 'activation_rate'),
            'EventEndRate': lambda conf: PlainModelFactory.simple(conf, 'process', 'deactivation_rate'),
            'InRate': lambda conf: PlainModelFactory.simple(conf, 'scheduler', 'on_rate'),
            'OffRate': lambda conf: PlainModelFactory.simple(conf, 'scheduler', 'off_rate'),
            'DetectionProb': lambda conf: PlainModelFactory.indexed(conf, 'sensors', 0, 'detection_probability'),
            'UnDetectionProb': lambda conf: 1 - PlainModelFactory.indexed(conf, 'sensors', 0, 'detection_probability')
        },
        'two': {
            'EventStartRate': lambda conf: PlainModelFactory.simple(conf, 'process', 'activation_rate'),
            'EventEndRate': lambda conf: PlainModelFactory.simple(conf, 'process', 'deactivation_rate'),
            'InRate': lambda conf: PlainModelFactory.simple(conf, 'scheduler', 'on_rate'),
            'OffRate': lambda conf: PlainModelFactory.simple(conf, 'scheduler', 'off_rate'),
            'InRate_2': lambda conf: PlainModelFactory.simple(conf, 'scheduler', 'on_rate'),
            'OffRate_2': lambda conf: PlainModelFactory.simple(conf, 'scheduler', 'off_rate'),
            'DetectionProb_1': lambda conf: PlainModelFactory.indexed(conf, 'sensors', 0, 'detection_probability'),
            'UnDetectionProb_1': lambda conf: 1 - PlainModelFactory.indexed(conf, 'sensors', 0,
                                                                            'detection_probability'),
            'DetectionProb_2': lambda conf: PlainModelFactory.indexed(conf, 'sensors', 1, 'detection_probability'),
            'UnDetectionProb_2': lambda conf: 1 - PlainModelFactory.indexed(conf, 'sensors', 1, 'detection_probability')
        },
        'three': {
            'EvenStartRate': lambda conf: PlainModelFactory.simple(conf, 'process', 'activation_rate'),
            'EventEndRate': lambda conf: PlainModelFactory.simple(conf, 'process', 'deactivation_rate'),
            'InRate_1': lambda conf: PlainModelFactory.simple(conf, 'scheduler', 'on_rate'),
            'OffRate_1': lambda conf: PlainModelFactory.simple(conf, 'scheduler', 'off_rate'),
            'InRate_2': lambda conf: PlainModelFactory.simple(conf, 'scheduler', 'on_rate'),
            'OffRate_2': lambda conf: PlainModelFactory.simple(conf, 'scheduler', 'off_rate'),
            'InRate_3': lambda conf: PlainModelFactory.simple(conf, 'scheduler', 'on_rate'),
            'OffRate_3': lambda conf: PlainModelFactory.simple(conf, 'scheduler', 'off_rate'),
            'DetectionProb_1': lambda conf: PlainModelFactory.indexed(conf, 'sensors', 0, 'detection_probability'),
            'UnDetectionProb_1': lambda conf: 1 - PlainModelFactory.indexed(conf, 'sensors', 0,
                                                                            'detection_probability'),
            'DetectionProb_2': lambda conf: PlainModelFactory.indexed(conf, 'sensors', 1, 'detection_probability'),
            'UnDetectionProb_2': lambda conf: 1 - PlainModelFactory.indexed(conf, 'sensors', 1,
                                                                            'detection_probability'),
            'DetectionProb_3': lambda conf: PlainModelFactory.indexed(conf, 'sensors', 2, 'detection_probability'),
            'UnDetectionProb_3': lambda conf: 1 - PlainModelFactory.indexed(conf, 'sensors', 2, 'detection_probability')
        }
    }

    measures = {
        'uno': {
            'safety': ['deactivation', 'able'],
            'sustainability': ['sensing']
        },
        'dos': {
            'safety': ['deactivation', 'able_1', 'able_2'],
            'sustainability': ['sensing_1', 'sensing_2']
        },
        'tres': {
            'safety': ['deactivation', 'able_1', 'able_2', 'able_3'],
            'sustainability': ['sensing_1', 'sensing_2', 'sensing_3']
        }
    }

    model_kb = {
        1: {
            'default': ('one_sensor', 'one', 'uno')
        },
        2: {
            'interleaved': ('two_interleaved', 'two', 'dos'),
            'most_effective': ('two_most_probable', 'two', 'dos'),
            'default': ('two_sensors', 'two', 'dos')
        },
        3: {'default': ('three_sensors', 'three', 'tres')}
    }

    @staticmethod
    def get_sensor_number(params):
        return len(list(params['sensors'].keys()))

    @staticmethod
    def get_sensor_number(params):
        return len(list(params['sensors'].keys()))

    @staticmethod
    def get_sensor_number(params):
        return len(list(params['sensors'].keys()))

    @staticmethod
    def generate(gspn_parameters, repository_folder):
        numbers: int = PlainModelFactory.get_sensor_number(gspn_parameters)
        default = PlainModelFactory.model_kb[numbers].get('default')
        scheduling_policy = gspn_parameters['scheduler']['kind']
        model_name, configuration_label, measures_label = PlainModelFactory.model_kb[numbers].get(scheduling_policy,
                                                                                                  default)
        configuration = PlainModelFactory.configurations[configuration_label]
        measures = PlainModelFactory.measures[measures_label]
        configuration_copy = configuration.copy()
        for key in configuration.keys():
            func = configuration[key]
            value = func(gspn_parameters)
            # configuration[key] = value       ERROR
            # In this way configuration is overwritten and it is not possible to have another iteration!!!
            configuration_copy[key] = value
        engine = Engine(model_name, repository_folder, configuration_copy, measures, gspn_parameters)
        return engine
