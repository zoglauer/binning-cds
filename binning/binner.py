import os
import pandas as pd

class Binner():
    def __init__(self, dataFile):
        ending = os.path.splitext(dataFile)[-1].lower()
        print(dataFile)
        if ending == ".pkl":
            self.df = pd.read_pickle(dataFile)
        else:
            self.df = pd.read_csv(dataFile)
    # def bin(binStyle):
        # test different binning methods - papers (+ references like qubo), ML based - train on simulation data, train with cone, physics based, occupancy based
    # def binID(self, phi, chi, psi):
    # def binValue(self, binID):
    # def binValue(self, phi, chi, psi):
    # def plot2d(self, param):
    # def plot3d(self):