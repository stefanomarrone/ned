from itertools import product

from pgmpy.estimators import MaximumLikelihoodEstimator
from pgmpy.inference import VariableElimination
from pgmpy.models import BayesianNetwork


class Network:
    def __init__(self, sensor_names):
        self.sensor_faults = None
        self.place_consistent = None
        self.model = None
        self.sensor_names = sensor_names

    def build(self, result_table):
        self.place_consistent = self.detect_place_consistency(result_table)
        self.sensor_faults = self.detect_faulty_sensors(result_table)
        couples = self.get_network_structure()
        self.model = BayesianNetwork(couples)
        self.model.fit(result_table, estimator=MaximumLikelihoodEstimator)

    def detect_place_consistency(self, result_table):
        # Check if Place is consistently True or False
        return result_table['asset'].nunique() == 1

    def detect_faulty_sensors(self, result_table):
        sensor_faults = {}
        for sensor in self.sensor_names:
            if result_table[sensor].nunique() == 1:  # Sensor always outputs the same value
                # If Place is also consistent, the sensor may not be faulty
                if not self.place_consistent:
                    sensor_faults[sensor] = result_table[sensor].iloc[0]  # Mark as faulty
        return sensor_faults

    def get_network_structure(self):
        asset_names = ['asset']
        couples = list(product(self.sensor_names, asset_names))
        return couples

    def analysis(self):
        # This kind of algorithm provides a probability P(si) = 1 when a sensor outputs always True
        # in order to prevent this, it is necessary to implement a faulty sensors detector that check
        # the behaviour of a sensor and penalise it when outputs always the same value (that is not correlated with
        # Place)
        detection = {}
        ve = VariableElimination(self.model)
        # @TODO
        # When the asset is protected e.g. its value is always False the ve.query fails.
        # In this edge case we can't find a correct value for the sensing probabilities:
        # If a sensor works perfectly (psensing ==1) but the asset is protected (its tolerance == +inf)
        # the sensing prob is useless. To correct in future works
        try:
            result = ve.query(variables=self.sensor_names, evidence={'asset': True}, joint=False)
            for name in self.sensor_names:
                distro = result[name]
                if name in self.sensor_faults:
                    detection[name] = 0  # Faulty sensor, balanced probability
                else:
                    index = distro.name_to_no[name][True]
                    probability = distro.values[index]
                    detection[name] = probability
        except Exception as e:
            print(e)
            raise
        return detection
