from gspn_model.gspn_naive_handle import generic_analysis
from utils.configuration import Configuration


class Engine:
    def __init__(self, model, model_repo, configuration):
        self.model = model
        self.model_configuration = configuration
        self.model_repo = model_repo
        config = Configuration()
        self.gspn_bin_path = config.get('greatspn')  # todo: use the parameter and make run general

    def getParamList(self):
        retval = list()
        for key in self.model_configuration.keys():
            retval.extend(['-rpar', key, str(self.model_configuration[key])])
        return retval

    def execute(self):
        generic_analysis(self.model, self.model_repo, self.getParamList())
