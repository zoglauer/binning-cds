# takes in the pkl file and splits it into a dataframe containing Energy, Theta (Polar Angle), Phi (Azimuthal), Scatter Angle, and Path length (cm). Code from Spring 2023

import pandas as pd # For data
import matplotlib.pyplot as plt # Plots
import numpy as np
import pickle

def filesplit(filepath = "/volumes/selene/users/andreas/simulationScript/Output/TestSource.926.inc1.id1.tra.gz.pkl"):
  fil = open(filepath, "rb")
  unpickled = pickle.load(fil)
  
  stuff = pickle.load(fil)
  arr = np.array(stuff)
  fil.close()
  
  
  df = pd.DataFrame(arr)
  df.rename(
      columns = {1: "Energy", 2: "Theta (Polar Angle)", 3: "Phi (Azimuthal)", 4: "Scatter Angle", 5: "Path Length (cm)"},
      inplace = True,
  )
  
  #datafile = open("./unpickler_output.txt", "r")
  data_all_strings = str(stuff)
  data_somewhat_list = data_all_strings.replace('\n', '').split(']')
  def parsenum(i):
    try:
      n = float(i)
    except:
      n = float("NaN")
  
    return n
  
  data = {}
  for i in np.arange(6):
    lst =  data_somewhat_list[i].split(',')
    lst[0] = lst[0].replace('[', '')
    lst = tuple(map(parsenum, lst))
    data[i] =  lst
  
  del data[0] # length is off by 1 and column is not entirely relevant
  df = pd.DataFrame(data)
  df.rename(
      columns = {1: "Energy", 2: "Theta (Polar Angle)", 3: "Phi (Azimuthal)", 4: "Scatter Angle", 5: "Path Length (cm)"},
      inplace = True,
      )
  return df
