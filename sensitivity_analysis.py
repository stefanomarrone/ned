import copy
import json
import math
import random

import numpy as np

from main import core
from utils.configuration import Configuration
import pandas as pd

c_default = {
    'main': {
        'hazardlevel': 2850,
        'asset': (4, 0),
        'simulation_steps': 1000,
        'outfolder': 'output/',
        'sensors': ['S1', 'S2'],
        'process': 'file',
        'scheduling': 'independent',
        'greatspn_project': 'repository',
        'greatspn_bin': '/Applications/GreatSPN.app/Contents/app/portable_greatspn/bin'

    },
    'process': 'file',
    'file': {
        'kind': 'csv',
        'filepath': 'data/',
        'filename': 'PREDIS009_process.csv'

    },
    'scheduler': {
        'on_rate': 0.0000462962963,
        'off_rate': 0.005555555556
    },

    'S1': {
        'threshold': 2900,
        'position': (3, 3),
        'mu': 0,
        'sigma': 150
    },
    'S2': {
        'threshold': 6000,
        'position': (2, 2),
        'mu': 0,
        'sigma': 300

    }
}


# lo tengo acceso per on_time (ore), lo accendo dopo off_time  (ore)
def times_to_rates(on_time, off_time):
    on_rate = 1 / (on_time * 60 * 60)
    off_rate = 1 / (off_time * 60 * 60)
    return on_rate, off_rate


"""
    Genero le configurazioni per la sensitivity analysis
    parto da una configurazione base che comprende un solo asset nel quale bisogna definire l'hazardlevel;
    uno scheduling indipendente nel quale bisogna definire on e off rate;
    DUE sensori (S1, S2) per i quali bisogna definire posizione, threshold e sigma.
    Iterando sulle variabili si esegue una brute-force generation che mostrerà il modo in cui MToT e ISL cambiano
"""

c_base = {
    'main': {
        'hazardlevel': None,  # 2850
        'asset': (4, 0),
        'simulation_steps': 1000,
        'outfolder': 'output/',
        'sensors': ['S1', 'S2'],
        'process': 'file',
        'scheduling': 'independent',
        'greatspn_project': 'repository',
        'greatspn_bin': '/Applications/GreatSPN.app/Contents/app/portable_greatspn/bin'

    },
    'process': 'file',
    'file': {
        'kind': 'csv',
        'filepath': 'data/',
        'filename': 'PREDIS009_process.csv'

    },
    'scheduler': {
        'on_rate': None,  # 0.0000462962963,
        'off_rate': None  # 0.005555555556
    },

    'S1': {
        'threshold': None,  # 2900,
        'position': (3, 3),
        'mu': 0,
        'sigma': None  # 150
    },
    'S2': {
        'threshold': None,  # 6000,
        'position': (2, 2),
        'mu': 0,
        'sigma': None,  # 300

    }
}
variables = {
    'main': {
        'hazardlevel': {
            'range': (1000, 3000)
        }
    },
    'scheduler': {
        'on_rate': {  # tempo che passa tra una misura e un'altra
            'range': (0.3333, 6)  # 20 minuti, 6h
        },
        'off_rate': {  # tempo passato a misurare
            'range': (0.05, 1),  # 3 minuti a 1 h
        }
    },
    'S1': {
        'threshold': {
            'range': (1000, 5000),
        },
        'sigma': {
            'range': (100, 300)
        }
    },
    'S2': {
        'threshold': {
            'range': (3000, 8000),
        },
        'sigma': {
            'range': (250, 450)
        }
    }
}


def sample_variable(variable_range):
    """Randomly sample a value from the given range."""
    return random.uniform(variable_range[0], variable_range[1])


def populate_configuration(c_base, variables):
    """Populate the configuration with sampled values."""
    config = copy.deepcopy(c_base)  # Create a deep copy to avoid modifying the original object

    # Sample and populate values
    config['main']['hazardlevel'] = sample_variable(variables['main']['hazardlevel']['range'])
    config['scheduler']['on_rate'], config['scheduler']['off_rate'] = times_to_rates(
        sample_variable(variables['scheduler']['on_rate']['range']),
        sample_variable(variables['scheduler']['off_rate']['range']))
    config['S1']['threshold'] = sample_variable(variables['S1']['threshold']['range'])
    config['S1']['sigma'] = sample_variable(variables['S1']['sigma']['range'])
    config['S2']['threshold'] = sample_variable(variables['S2']['threshold']['range'])
    config['S2']['sigma'] = sample_variable(variables['S2']['sigma']['range'])

    return config


def monte_carlo_simulation(c_base, variables, num_iterations):
    """Perform a Monte Carlo simulation."""
    results = []
    for _ in range(num_iterations):
        config = populate_configuration(c_base, variables)
        results.append(config)
    return results


def oat_sensitivity_analysis(c_base, variables, num_samples_per_param):
    """
    Perform One-at-a-Time (OAT) sensitivity analysis, generating configurations.

    Args:
        c_base: Base configuration dictionary.
        variables: Dictionary defining parameter ranges.
        num_samples_per_param: Number of samples for each parameter being varied.

    Returns:
        A list of configurations for the core function.
    """
    configurations = []

    for section, params in variables.items():
        for param, details in params.items():
            # Create a base configuration with randomly sampled fixed values
            fixed_config = populate_configuration(c_base, variables)

            # Systematically vary the current parameter
            param_values = [
                details['range'][0] + (i / (num_samples_per_param - 1)) * (details['range'][1] - details['range'][0])
                for i in range(num_samples_per_param)
            ]

            for value in param_values:
                # Update the current parameter
                config = copy.deepcopy(fixed_config)
                if section in config and param in config[section]:
                    config[section][param] = value
                elif section in config and isinstance(config[section], dict):
                    config[section][param] = value

                # Add configuration to the list
                configurations.append(config)
    return configurations


def run_monte_carlo(configurations, num_configs):
    configurations.extend(monte_carlo_simulation(c_base, variables, num_configs))
    mtots = []
    isls = []
    # configurations = []
    resobj = []
    ok_configurations = []
    for c in configurations:
        # leggo configurazioni e creo file temporanei
        configuration = Configuration().init_from_content(c)
        mtot, isl = core(configuration_filename='', draw_flag=draw_flag, ext_configuration=configuration)
        if mtot != math.inf or isl != -math.inf:
            mtots.append(mtot)
            isls.append(isl)
            c['mtot'] = mtot
            c['isl'] = isl
            resobj.append(c)
            ok_configurations.append(c)
            print(mtot, isl)

    return ok_configurations, mtots, isls, resobj


def run_oat_analysis(configurations, num_samples_per_param):
    """
    Run OAT sensitivity analysis and process configurations with the core function.

    Args:
        c_base: Base configuration dictionary.
        variables: Dictionary defining parameter ranges.
        num_samples_per_param: Number of samples for each parameter being varied.

    Returns:
        ok_configurations, mtots, isls, resobj: Results from the core function.
    """
    # Generate OAT configurations
    configurations.extend(oat_sensitivity_analysis(c_base, variables, num_samples_per_param))
    print(len(configurations))
    mtots = []
    isls = []
    resobj = []
    ok_configurations = []

    for c in configurations:
        # Create configuration object for the core function
        configuration = Configuration().init_from_content(c)
        mtot, isl = core(configuration_filename='', draw_flag=False, ext_configuration=configuration)

        if mtot != math.inf and isl != -math.inf:
            mtots.append(mtot)
            isls.append(isl)
            c['mtot'] = mtot
            c['isl'] = isl
            resobj.append(c)
            ok_configurations.append(c)
            print(mtot, isl)
            print(f"mtot: {mtot}, isl: {isl}")

    return ok_configurations, mtots, isls, resobj


def save_to_csv(data, output_csv_path):
    rows = []
    for entry in data:
        row = {
            'mtot': entry['mtot'],
            'isl': entry['isl'],
            'main_hazardlevel': entry['main']['hazardlevel'],
            'scheduler_on_rate': entry['scheduler']['on_rate'],
            'scheduler_off_rate': entry['scheduler']['off_rate'],
            'S1_threshold': entry['S1']['threshold'],
            'S1_sigma': entry['S1']['sigma'],
            'S2_threshold': entry['S2']['threshold'],
            'S2_sigma': entry['S2']['sigma']
        }
        rows.append(row)

    # Convert to DataFrame
    df = pd.DataFrame(rows)

    # Save to CSV
    df.to_csv(output_csv_path, index=False)


if __name__ == "__main__":
    draw_flag = False
    save = True
    # Run MCA
    num_configs = 0
    configurations = []  # c_default]
    ok_configurations, mtots, isls, resobj = run_monte_carlo(configurations, num_configs)
    for z in zip(ok_configurations, mtots, isls):
        print(z)
    if mtots:
        pos_min_mtot = np.argmin(mtots)
        print('minimo: ', mtots[pos_min_mtot])
        print('configurazione: ', ok_configurations[pos_min_mtot])
        if save:
            save_to_csv(ok_configurations, 'res_mca.csv')
    else:
        print("No mtot")

    configurations = [c_default]
    ok_configurations, mtots, isls, resobj = run_oat_analysis(configurations, num_samples_per_param=100)
    for z in zip(ok_configurations, mtots, isls):
        print(z)
    if mtots:
        pos_min_mtot = np.argmin(mtots)
        print('minimo: ', mtots[pos_min_mtot])
        print('configurazione: ', ok_configurations[pos_min_mtot])
        if save:
            save_to_csv(ok_configurations, 'res_ota.csv')
    else:
        print("No mtot")
