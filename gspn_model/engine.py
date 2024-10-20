import os

from gspn_model.gspn_naive_handle import GSPN_handler
from utils.configuration import Configuration
import ctypes


class Engine:
    def __init__(self, model, model_repo, configuration, measures, gspn_parameters=None):
        self.model = model
        self.model_configuration = configuration
        self.model_repo = model_repo
        self.measures = measures
        config = Configuration()
        self.gspn_bin_path = config.get('greatspn')  # todo: use the parameter and make run general
        self.gspn_parameters = gspn_parameters
        self.gspn_handler: GSPN_handler = GSPN_handler(greatspn_scripts=self.gspn_bin_path)

    def getParamList(self):
        retval = list()
        for key in self.model_configuration.keys():
            retval.extend(['-rpar', key, str(self.model_configuration[key])])
        return retval

    def execute(self):
        self.gspn_handler.generic_analysis(self.model, self.model_repo, self.getParamList())

    def safety(self):
        transition_names = self.measures['safety']
        values = list(map(self.get_throughput, transition_names))
        retval = 1 / sum(values)
        return retval

    def sustainability(self):
        place_names = self.measures['sustainability']
        values = list(map(self.__c_readtpd_wrapper, place_names))
        values = list(map(lambda x: 1 / x, values))
        retval = min(values)
        return retval

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
                raise Exception("Node not found")
        except FileNotFoundError:
            print("File not found")

    def get_throughput(self, transition_name: str) -> float:
        line_header = 'Thru_' + transition_name
        netpath = f'{os.getcwd()}/{self.model_repo}/{self.model}_analysis'
        trovato: bool = False
        retval = None
        try:
            with open(f'{netpath}/{self.model}.sta', 'r') as grg_file:
                while (not trovato):
                    line = grg_file.__next__()
                    if line_header in line:
                        elements = line.split(' ')
                        retval = float(elements[2])
                        trovato = True
            if trovato is False:
                print(f'Error {transition_name}')
                raise Exception('Thru not found')
        except FileNotFoundError:
            print("File not found")
        return retval
