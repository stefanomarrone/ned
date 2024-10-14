import subprocess
from enum import Enum
from typing import List

import numpy as np


def run_greatspn(model_name, procedure, params, greatspn_scripts="/opt/greatspn/lib/app/portable_greatspn/bin/"):
    """
    Function to run any GREATSPN procedure with customizable parameters.

    :param model_name: Name of the model (e.g., 'Shared').
    :param procedure: Name of the GREATSPN procedure to execute (e.g., 'WNRG', 'swn_stndrd').
    :param params: List of parameters for the procedure (each parameter and its value as separate items in the list).
    :param greatspn_scripts: Path to the directory containing GREATSPN binaries.
    """
    # Build the full command
    command = [f"{greatspn_scripts}/{procedure}"] + [model_name] + params
    print(f"Executing: {' '.join(command)}")  # For debugging purposes
    # Run the command
    subprocess.run(command)


"""
OLD EXAMPLE 

# Call WNRG procedure with custom parameters
run_greatspn(model_name, 'WNRG',
             ['-mpar', 'CHload', '2', '-mpar', 'CHparallel', '4', '-rpar', 'Pfraud', '8.5', '-m', '-gui-stat', '-dot-F',
              f"{model_name}-RG-0", '-max-dot-markings', '80'])

# Clear .gst file
subprocess.run(["cp", "/dev/null", f"{model_name}.gst"])

# Call swn_stndrd
run_greatspn(model_name, 'swn_stndrd', [])

# Call swn_ggsc with its parameters
run_greatspn(model_name, 'swn_ggsc', ['-e1.0E-7', '-i10000'])

# Copy .epd to .mpd
subprocess.run(["cp", f"{model_name}.epd", f"{model_name}.mpd"])

# Call swn_gst_prep with different parameters
run_greatspn(model_name, 'swn_gst_prep', ['-mpar', 'CHload', '2', '-mpar', 'CHparallel', '4', '-rpar', 'Pfraud', '8.5'])

# Call swn_gst_stndrd
run_greatspn(model_name, 'swn_gst_stndrd', ['-append', f"{model_name}.sta"])
"""


class OpType(Enum):
    gspn = 'GSPN'
    cmd = 'CMD'


class Operation:
    def __init__(self, op_type: OpType, name, parameters=None):
        self.type = op_type
        self.name = name
        self.parameters = parameters


def run_steady_state_analysis(model_name, parameters):
    extended_pars = parameters
    extended_pars.extend([
        '-m',
        '-gui-stat', '-dot-F',
        f"{model_name}-RG-0", '-max-dot-markings', '80'])
    operations = [
        # Call WNRG procedure with custom parameters
        Operation(op_type=OpType.gspn, name='WNRG',
                  parameters=extended_pars),
        # Clear .gst file
        Operation(op_type=OpType.cmd, name=["cp", "/dev/null", f"{model_name}.gst"]),
        # Call swn_stndrd
        Operation(op_type=OpType.gspn, name='swn_stndrd', parameters=[]),
        # Call swn_ggsc with its parameters
        Operation(op_type=OpType.gspn, name='swn_ggsc', parameters=['-e1.0E-7', '-i10000']),
        # Copy .epd to .mpd
        Operation(op_type=OpType.cmd, name=["cp", f"{model_name}.epd", f"{model_name}.mpd"]),
        # Call swn_gst_prep with different parameters
        Operation(op_type=OpType.gspn, name='swn_gst_prep',
                  parameters=parameters),
        # Call swn_gst_stndrd
        Operation(op_type=OpType.gspn, name='swn_gst_stndrd', parameters=['-append', f"{model_name}.sta"])
    ]
    for op in operations:
        if op.type == OpType.gspn:
            run_greatspn(model_name, op.name,
                         op.parameters)
        else:
            subprocess.run(op.name)


# @TODO: find a way to use the gspn_modelfactory
def one_sensor_analysis(detection_prob, event_end_rate, event_start_rate, on_rate, off_rate):
    model_name = 'models/one_sensor'

    run_steady_state_analysis(model_name=model_name,
                              parameters=['-rpar', 'DetectionProb', str(detection_prob), '-rpar', 'EventEndRate',
                                          str(event_end_rate), '-rpar', 'EventStartRate',
                                          str(event_start_rate), '-rpar', 'InRate', str(on_rate), '-rpar', 'OffRate',
                                          str(off_rate), ])


if __name__ == '__main__':
    one_sensor_analysis(detection_prob=np.float64(0.59),
                        event_end_rate=0.97,
                        event_start_rate=0.03,
                        on_rate=0.0001,
                        off_rate=0.1)
