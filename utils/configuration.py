from metaclasses import Singleton
from configparser import ConfigParser
import configparser

class Configuration(metaclass=Singleton):
    def __init__(self, inifilename):
        self.board = dict()
        self.load(inifilename)

    def get(self, key):
        return self.board[key]

    def put(self, key, value):
        self.board[key] = value

    @staticmethod
    def tolist(value):
        retval = value.split(',')
        return retval

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

    def loadIndices(self,reader):
        temp = dict()
        options = reader.options("indices")
        for o in options:
            value = reader["indices"][o]
            temp[o] = self.tolist(value)
        retval = dict()
        retval["indices"] = temp
        return retval

    def loadDetails(self,reader):
        temp = dict()
        options = reader.options("details")
        for o in options:
            value = reader["details"][o]
            temp[o] = self.tolist(value)
        retval = dict()
        retval["details"] = temp
        return retval

    def load(self,inifile):
        reader = ConfigParser()
        reader.read(inifile)
        try:
            temp = reader['main']['output']
            self.put('output',temp)
            temp = reader['main']['logfilename']
            self.put('logfilename',temp)
            temp = reader['main']['logpolicy']
            self.put('logpolicy',temp)
            temp = self.tolist(reader['main']['period'])
            self.put('startingmonth',temp[0])
            self.put('endmonth',temp[1])
            #constraintfile = self.tolist(reader['main']['constraints'])
            chapterList = self.tolist(reader['main']['chapters'])
            self.put('chapters',chapterList)
            for ch in chapterList:
                temp = self.loadSection(reader, ch)
                self.board.update(temp)
            temp = self.loadIndices(reader)
            self.board.update(temp)
            temp = self.loadDetails(reader)
            self.board.update(temp)
        except Exception as s:
            print(s)
