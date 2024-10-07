class ModelAbstractFactory:
    @staticmethod
    def generate(gspn_parameters, model_project):
        pass


class ModelNonComposableFactory:

    configurations = {
        'one': {},

    }

    # todo: completare popolamento KB
    model_kb = {
        1: {
            'default': ('one_sensor', 'one')
        },
        2: {
            'interleaved': ('two_interleaved', {}),
            'most_effective': ('most_effective', {}),
            'default': ('two_sensor', {})
        },
        3: {'default': ('three_sensors', {})}
    }

    @staticmethod
    def generate(gspn_parameters, model_project):
        pass
