import sys
import os
import pandas as pd
import pickle

sys.path.append(os.path.join(os.path.dirname(sys.path[0]),"binning"))
from binner import Binner

# testDataFile = "/volumes/selene/users/andreas/simulationScript/Output/TestSource.999.inc1.id1.tra.gz.pkl"
# binny = Binner(testDataFile)
# print(binny.df)

binny = Binner()
x = binny.filesplit()
y = binny.binnertest(x, 20, 20, colnames=['theta','phi','scatterangle'])
print(y.head())

