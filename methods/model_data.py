from methods import DataModel
from methods.plots import Plots

class StGallen(DataModel):
    def __init__(self):
        super().__init__()

    def plot_data(self):
        self.plots.prepare_figure()
        self.plots.plot_figure()
    
    def save_data(self, output_path='output/Dashboard.html'):
        self.plots.prepare_figure()
        self.plots.save_figure(output_path)
        