from itertools import product

from pgmpy.estimators import MaximumLikelihoodEstimator
from pgmpy.inference import VariableElimination
from pgmpy.models import BayesianNetwork


class Network:
    def __init__(self, sensor_names):
        self.model = None
        self.sensor_names = sensor_names

    def build(self, result_table):
        couples = self.get_network_structure()
        self.model = BayesianNetwork(couples)
        self.model.fit(result_table, estimator=MaximumLikelihoodEstimator)

    def get_network_structure(self):
        asset_names = ['asset']
        couples = list(product(self.sensor_names,asset_names))
        return couples

    def analysis(self):
        detection = {}
        ve = VariableElimination(self.model)
        try:
            result = ve.query(variables=self.sensor_names, evidence={'asset': True}, joint=False)
            for name in self.sensor_names:
                distro = result[name]
                index = distro.name_to_no[name][True]
                probability = distro.values[index]
                detection[name] = probability
        except Exception as e:
            pass
        return detection
