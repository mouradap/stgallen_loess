from abc import ABC
from abc import abstractmethod
from methods.preprocess import DataProcessor
from methods.plots import Plots

data_proc = DataProcessor()

class DataModel(ABC):
    def preprocess(self, data):
        self.data = data_proc.process_data(data)
        self.plots = Plots(self.data)

    @abstractmethod
    def plot_data(self, func):
        pass