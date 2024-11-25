import glob
import os
import subprocess
from enum import Enum
import copy
from typing import Union
import numpy as np
from utils.metaclasses import Singleton
import shutil

from utils.utils import clear_folder


class OpType(Enum):
    gspn = 'GSPN'
    cmd = 'CMD'


class Operation:
    def __init__(self, op_type: OpType, name, parameters=None):
        self.type = op_type
        self.name = name
        self.parameters = parameters


class GSPN_handler(metaclass=Singleton):
    def __init__(self, greatspn_scripts: Union[str, None] = "/opt/greatspn/lib/app/portable_greatspn/bin/"):
        self.greatspn_scripts = greatspn_scripts

    def __run_greatspn(self, model_name, procedure, params):
        """
        Function to run any GREATSPN procedure with customizable parameters.

        :param model_name: Name of the model (e.g., 'Shared').
        :param procedure: Name of the GREATSPN procedure to execute (e.g., 'WNRG', 'swn_stndrd').
        :param params: List of parameters for the procedure (each parameter and its value as separate items in the list).
        :param greatspn_scripts: Path to the directory containing GREATSPN binaries.
        """
        # Build the full command
        command = [f"{self.greatspn_scripts}/{procedure}"] + [model_name] + params
        print(f"Executing: {' '.join(command)}")  # For debugging purposes
        # Run the command
        subprocess.run(command)

    def run_steady_state_analysis(self, model_name, parameters):
        extended_pars = copy.deepcopy(parameters)
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
                self.__run_greatspn(model_name, op.name,
                                    op.parameters)
            else:
                subprocess.run(op.name)

    # @TODO: find a way to use the gspn_modelfactory
    def one_sensor_analysis(self, detection_prob, event_end_rate, event_start_rate, on_rate, off_rate):
        model_name = 'one_sensor'
        try:
            # making the directory
            path = f'{os.getcwd()}/models/{model_name}_analysis'
            os.makedirs(path, exist_ok=True)
            # moving all the file here
            shutil.copy(f'models/{model_name}.def', path)
            shutil.copy(f'models/{model_name}.net', path)

            model_name = f'{path}/{model_name}'
        except Exception as e:
            print(e)
            raise
        self.run_steady_state_analysis(model_name=model_name,
                                       parameters=['-rpar', 'DetectionProb', str(detection_prob), '-rpar',
                                                   'EventEndRate',
                                                   str(event_end_rate), '-rpar', 'EventStartRate',
                                                   str(event_start_rate), '-rpar', 'InRate', str(on_rate), '-rpar',
                                                   'OffRate',
                                                   str(off_rate)])

    def generic_analysis(self, model_name, model_repo, parameter_list):
        try:
            # removing the directory
            path = f'{os.getcwd()}/{model_repo}/{model_name}_analysis'
            existing = os.path.isdir(path)
            if not existing:
                os.makedirs(path, exist_ok=True)
            else:
                files = glob.glob(path + '/*')
                for f in files:
                    os.remove(f)
            # moving all the file here
            shutil.copy(f'{os.getcwd()}/{model_repo}/{model_name}.def', path)
            shutil.copy(f'{os.getcwd()}/{model_repo}/{model_name}.net', path)
            model_name = f'{path}/{model_name}'
        except Exception as e:
            print(e)
            raise
        self.run_steady_state_analysis(model_name=model_name, parameters=parameter_list)


if __name__ == '__main__':
    gspn_handler = GSPN_handler(greatspn_scripts='/Applications/GreatSPN/Contents/app/portable_greatspn/bin/')
    gspn_handler.one_sensor_analysis(detection_prob=np.float64(0.59),
                                     event_end_rate=0.97,
                                     event_start_rate=0.03,
                                     on_rate=0.0001,
                                     off_rate=0.1)
