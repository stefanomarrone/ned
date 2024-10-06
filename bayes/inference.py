from itertools import product
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pgmpy.models import BayesianNetwork
from pgmpy.estimators import MaximumLikelihoodEstimator
from pgmpy.inference import VariableElimination
import networkx as nx
from configparser import ConfigParser
import sys

class Network:
    def __init__(self, sensor_names):
        self.model = None
        self.sensor_names = sensor_names

    def build(self, result_table):
        couples = self.get_network_structure()
        self.model = BayesianNetwork(couples)
        self.model.fit(result_table, estimator=MaximumLikelihoodEstimator)
        #todo: complete with network a posteriori inference
        pass


    def get_network_structure(self):
        asset_names = ['asset']
        couples = list(product(self.sensor_names,asset_names))
        return couples
