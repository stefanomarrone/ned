from utils.metaclasses import Singleton
from configparser import ConfigParser
import configparser
import tempfile
import io

from utils.utils import tostring


class Configuration(metaclass=Singleton):
    def __init__(self, inifilename):
        self.board = dict()
        content = self.preprocess(inifilename)
        self.load(content)

    def get(self, key):
        return self.board[key]

    def put(self, key, value):
        self.board[key] = value

    def loadSection(self,reader,s):
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

    def load(self, content):
        reader = ConfigParser()
        inifile = io.StringIO(content)
        reader.read_file(inifile)
        try:
            temp = int(reader['main']['hazardlevel'])
            self.put('hazardlevel',temp)
            #todo load the configuration
            temp = int(reader['main']['hazardlevel'])
            self.put('output',temp)
            temp = int(reader['main']['hazardlevel'])
            self.put('output',temp)
            temp = int(reader['main']['hazardlevel'])
            self.put('output',temp)
        except Exception as s:
            print(s)

    def preprocess(self, inifile):
        content = tostring(inifile)
        reader = ConfigParser()
        reader.read(inifile)
        try:
            temp = reader['main']['sensor_ini']
            content += '\n' + tostring(temp)
            temp = reader['main']['process_ini']
            content += '\n\n' + tostring(temp)
        except Exception as s:
            print(s)
        return content


