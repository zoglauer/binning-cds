import sys
import os
import pandas as pd
import pickle

sys.path.append(os.path.join(os.path.dirname(sys.path[0]),"binning"))
from binner import Binner

# testDataFile = "/volumes/selene/users/andreas/simulationScript/Output/TestSource.999.inc1.id1.tra.gz.pkl"
# binny = Binner(testDataFile)
# print(binny.df)

filepath = "/volumes/selene/users/andreas/simulationScript/Output/TestSource.926.inc1.id1.tra.gz.pkl"
binny = Binner(filepath)
# x = binny.binnertest(binny.df, 20, 20)
# print(x.head())

# x = binny.filesplit()
# y = binnertest(x, 20, 20, colnames=['theta','phi','scatterangle'])
# print(y.head())
