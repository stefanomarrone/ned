import configparser
import io
import os
from configparser import ConfigParser

from utils.metaclasses import Singleton
from utils.utils import tostring


class Configuration(metaclass=Singleton):
    process_registry = {
        'spike': [('range', float), ('rate', float), ('mu', float), ('sigma', float), ('level', float)],
        'walk': [('drift', float), ('mu', float), ('sigma', float), ('level', float)],
        'file': [('filename', str), ('filepath', str)]
    }

    def __init__(self, inifilename=None):
        self.board = dict()
        if inifilename is not None:
            self.init_from_filename(inifilename)

    def init_from_filename(self, inifilename):
        content = self.preprocess(inifilename)
        reader = ConfigParser()
        inifile = io.StringIO(content)
        reader.read_file(inifile)
        self.load(reader)

    def init_from_content(self, content):
        self.load(content)
        return self
        # raise Exception('Not yet implemented')

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
    def load(self, reader):
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
            if type(temp) is str:
                temp = temp.split(',')
                temp = tuple([float(i) for i in temp])
            self.put('asset', temp)
            temp = reader['main']['sensors']
            if type(temp) is str:
                sensors = list(temp.split(','))
            else:
                sensors = temp
            self.put('sensors', sensors)
            temp = reader['main']['process']
            self.put('process', temp)
            # Sensors configuration
            for sensor in sensors:
                sensor_parameters = dict()
                temp = float(reader[sensor]['threshold'])
                sensor_parameters['threshold'] = temp
                temp = reader[sensor]['position']
                if type(temp) is str:
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

        includes = reader['main']['include'].split(',')
        # imposto infolder per i file .ini
        if 'infolder' in reader['main']:
            infolder = reader['main']['infolder']
        else:
            infolder = os.getcwd()
        for include in includes:
            content += '\n' + tostring(f'{infolder}{include}')

        return content
