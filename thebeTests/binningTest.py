import sys
import os
import pandas as pd
import pickle
import psutil

sys.path.append(os.path.join(os.path.dirname(sys.path[0]),"binning"))
from binner import Binner

filepath = "/volumes/selene/users/andreas/simulationScript/Output/TestSource.999.inc1.id1.tra.gz.pkl"
# filepath = "/volumes/selene/users/joseph/simulationScript/simulationResults/FlatContinuumIsotropic.inc381.id1.tra.gz.pkl"
binny = Binner(filepath)
# binny.bin()
# binny.getBinBounds()
binny.bin3D()
print(psutil.Process(os.getpid()).memory_info().rss / 1024 ** 2, "MiB")
# print("Theta Bins")
# binny.printBins(20, "Theta")
# print()
# print("Phi Bins")
# binny.printBins(20, "Phi")
# print()
# print("Scatter Angle Bins")
# binny.printBins(20, "Scatter Angle")
#test
