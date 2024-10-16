import os

from gspn_model.gspn_naive_handle import generic_analysis
from utils.configuration import Configuration
import ctypes


class Engine:
    def __init__(self, model, model_repo, configuration, gspn_parameters = None):
        self.model = model
        self.model_configuration = configuration
        self.model_repo = model_repo
        config = Configuration()
        self.gspn_bin_path = config.get('greatspn')  # todo: use the parameter and make run general
        self.gspn_parameters = gspn_parameters

    def getParamList(self):
        retval = list()
        for key in self.model_configuration.keys():
            retval.extend(['-rpar', key, str(self.model_configuration[key])])
        return retval

    def execute(self):
        generic_analysis(self.model, self.model_repo, self.getParamList())

    def safety(self, node_name):
        if self.gspn_parameters is not None:
            return self.__c_readtpd_wrapper(node_name) * self.gspn_parameters['process']['deactivation_rate']
        print("No global parameters injected")

    def sustainability(self):
        pass

    def __c_readtpd_wrapper(self, node_name) -> float:
        c_library = ctypes.CDLL(f'{os.getcwd()}/gspn_model/readtpd.so')
        get_average_wrapper = c_library.get_average
        get_average_wrapper.argtypes = [ctypes.c_char_p, ctypes.c_int]
        get_average_wrapper.restype = ctypes.c_float
        netpath = f'{os.getcwd()}/{self.model_repo}/{self.model}_analysis'
        trovato: bool = False
        node_id = -1
        try:
            with open(f'{netpath}/{self.model}.grg', 'r') as grg_file:
                for line in grg_file:
                    if node_name in line:
                        node_id = int(line[0])
                        trovato = True
                        break
            if trovato:
                netname = f'{netpath}/{self.model}'
                netname_bytes = netname.encode('utf-8')
                avg = get_average_wrapper(netname_bytes, node_id)
                return avg
            else:
                raise "Node not found"
        except FileNotFoundError:
            print("File not found")
