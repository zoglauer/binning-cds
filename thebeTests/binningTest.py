import sys
import os
import pandas as pd
import pickle

sys.path.append(os.path.join(os.path.dirname(sys.path[0]),"binning"))
from binner import Binner

filepath = "/volumes/selene/users/andreas/simulationScript/Output/TestSource.926.inc1.id1.tra.gz.pkl"
# filepath = "/volumes/selene/users/joseph/simulationScript/simulationResults/FlatContinuumIsotropic.inc381.id1.tra.gz.pkl"
binny = Binner(filepath)
binny.bin()
binny.getBinBounds()
