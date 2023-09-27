import pickle
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
        
    # def binID(self, phi, chi, psi):
    # def binValue(self, binID):
    # def binValue(self, phi, chi, psi):
    # def plot(self):