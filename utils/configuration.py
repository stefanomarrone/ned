from torchgen.packaged.autograd.gen_autograd_functions import process_function

from utils.metaclasses import Singleton
from configparser import ConfigParser
import configparser
import io
from utils.utils import tostring


class Configuration(metaclass=Singleton):
    process_registry = {
        'spike': [('range', float), ('rate', float), ('mu', float), ('sigma', float), ('level', float)],
        'walk': [('drift', float), ('mu', float), ('sigma', float), ('level', float)]
    }

    def __init__(self, inifilename):
        self.board = dict()
        content = self.preprocess(inifilename)
        self.load(content)

    def get(self, key):
        return self.board[key]

    def put(self, key, value):
        self.board[key] = value

    def loadSection(self, reader, s):
        temp = dict()
        options = []
        try:
            options = reader.options(s)
        except configparser.NoSectionError as nse:
            temp[s] = ['*']
        for o in options:
            try:
                value = reader[s][o]
                temp[s] = self.tolist(value)
            except:
                print("exception on %s!" % o)
        return temp

    # todo: dynamic configuration ready for the process is not implemented, yet
    def load(self, content):
        reader = ConfigParser()
        inifile = io.StringIO(content)
        reader.read_file(inifile)
        try:
            # Main configuration
            temp = reader['main']['greatspn_bin']
            self.put('greatspn', temp)
            temp = reader['main']['greatspn_project']
            self.put('greatspn_repos', temp)
            temp = reader['main']['outfolder']
            self.put('outfolder', temp)
            temp = int(reader['main']['simulation_steps'])
            self.put('simulation_steps', temp)
            temp = float(reader['main']['hazardlevel'])
            self.put('hazardlevel', temp)
            temp = reader['main']['asset']
            temp = temp.split(',')
            temp = tuple([float(i) for i in temp])
            self.put('asset', temp)
            temp = reader['main']['sensors']
            sensors = list(temp.split(','))
            self.put('sensors', temp.split(','))
            temp = reader['main']['process']
            self.put('process', temp)
            # Sensors configuration
            for sensor in sensors:
                sensor_parameters = dict()
                temp = float(reader[sensor]['threshold'])
                sensor_parameters['threshold'] = temp
                temp = reader[sensor]['position']
                temp = temp.split(',')
                temp = tuple([float(i) for i in temp])
                sensor_parameters['position'] = temp
                temp = float(reader[sensor]['mu'])
                sensor_parameters['mu'] = temp
                temp = float(reader[sensor]['sigma'])
                sensor_parameters['sigma'] = temp
                self.put(sensor, sensor_parameters)
            # Process configuration
            process = reader['main']['process']
            process_elements = Configuration.process_registry[process]
            dictionary = {'kind': process}
            for element in process_elements:
                process_key, process_function = element
                value = reader[process][process_key]
                dictionary[process_key] = process_function(value)
            self.put('process', dictionary)
            # Scheduler configuration
            temp = reader['main']['scheduling']
            self.put('scheduler', temp)
            temp = float(reader['scheduler']['on_rate'])
            self.put('on_rate', temp)
            temp = float(reader['scheduler']['off_rate'])
            self.put('off_rate', temp)
        except Exception as s:
            print(s)

    def preprocess(self, inifile):
        content = tostring(inifile)
        reader = ConfigParser()
        reader.read(inifile)
        try:
            includes = reader['main']['include'].split(',')
            for include in includes:
                content += '\n' + tostring(include)
        except Exception as s:
            print(s)
        return content
