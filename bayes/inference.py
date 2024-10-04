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
    def __init__(self, ssensors, aasset, ddataset):
        self.asset = aasset
        self.sensors = ssensors
        self.dataset = ddataset
        self.model = None

    def get_network_structure(self):
        asset_names = list(self.asset.getName())
        sensor_names = list(map(lambda s: s.getName(), self.sensors))
        couples = list(product(sensor_names,asset_names))
        return couples

    def data_adjusting(self):
        pass #todo completare la funzione




    def inference(self, data):
        couples = self.get_network_structure()
        self.model = BayesianNetwork(couples)
        self.model.fit(self.data, estimator=MaximumLikelihoodEstimator)
