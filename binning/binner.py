import os
import pandas as pd
import numpy as np
import pickle
import time
from point import Point
class Binner():
    def __init__(self, dataFile):
        # start times for runtime analysis
        # self.start = time.time()
        self.bins = {}
        ending = os.path.splitext(dataFile)[-1].lower()
        if ending == ".pkl":
            self.lst = pd.read_pickle(dataFile)
        else:
            self.lst = pd.read_csv(dataFile)
        self.listSplit()

    def listSplit(self):
        # data = [self.lst[0], self.lst[1], self.lst[2], self.lst[3], self.lst[4], self.lst[5]]
        # self.df = pd.DataFrame(data).T.rename(columns={0: "Event ID", 1: "Energy", 2: "Theta", 3: "Phi", 4: "Scatter Angle", 5: "Path Length"})
        # RUNTIME TEST
        # print(self.df.head())
        # print("Method 1", time.time() - self.start)

        data = []
        for i in range(len(self.lst[0])):
            if (self.lst[1][i] < 507 or self.lst[1][i] > 515):
                continue
            # data.append(Point(self.lst[0][i], self.lst[1][i], self.lst[2][i], self.lst[3][i], self.lst[4][i], self.lst[5][i]))
            dataI = []
            dataI.append(self.lst[0][i])
            dataI.append(self.lst[1][i])
            dataI.append(self.lst[2][i])
            dataI.append(self.lst[3][i])
            dataI.append(self.lst[4][i])
            dataI.append(self.lst[5][i])
            data.append(dataI)
        self.df = pd.DataFrame(data, columns=["Event ID", "Energy", "Theta", "Phi", "Scatter Angle", "Path Length (cm)"])
        # # RUNTIME TEST
        # print(self.df.head(10))
        # print("Method 2", time.time() - self.start)

        # for data set "/volumes/selene/users/andreas/simulationScript/Output/TestSource.926.inc1.id1.tra.gz.pkl",
        # Method 1 took 71.73062920570374 seconds and Method 2 took 15.090354919433594
    
    def bin(self, n=20, column="Theta"):
        # x = time.time()
        self.bins[f"{column} {n}"] = []
        currDf = self.df.sort_values(by=column).reset_index(drop=False)
        # account for rebinning if values are the same
        binSize = len(currDf) // n
        overflow = len(currDf) -  n * binSize
        prev = 0
        curr = 0
        i = 0
        for i in range(n):
            if i < overflow:
                x = binSize + 1
            else:
                x = binSize
            curr = prev + x
            self.bins[f"{column} {n}"].append(currDf[prev:curr])
            prev = curr
        # print("Bin Runtime:", time.time() - x)
    
    def getBinBounds(self, n=20, column="Theta"):
        theBin = self.bins[f"{column} {n}"]
        lst = []
        for x in theBin:
            lst.append([list(x[column])[0], list(x[column])[-1]])
        return lst
    
    def getBinUpperBounds(self, n=20, column="Theta"):
        theBin = self.bins[f"{column} {n}"]
        lst = []
        for x in theBin:
            lst.append(list(x[column])[-1])
        return lst

    def bin3D(self, n=[20, 20, 20], columns=["Theta", "Phi", "Scatter Angle"]):
        DF = self.df
        x = time.time()
        self.bin(n[0], columns[0])
        self.bin(n[1], columns[1])
        self.bin(n[2], columns[2])
        bb1 = np.array(self.getBinUpperBounds(n[0], columns[0]))
        bb2 = np.array(self.getBinUpperBounds(n[1], columns[1]))
        bb3 = np.array(self.getBinUpperBounds(n[2], columns[2]))
        columnA = []
        columnB = []
        columnC = []
        for i in range(len(DF)):
            a = DF[columns[0]][i]
            a1 = list(bb1 < a).index(False)
            columnA.append(bb1.item(a1))
            b = DF[columns[1]][i]
            b1 = list(bb2 < b).index(False)
            columnB.append(bb2.item(b1))
            c = DF[columns[2]][i]
            c1 = list(bb3 < c).index(False)
            columnC.append(bb3.item(c1))
        DF[f"{columns[0]} Bin"] = columnA
        DF[f"{columns[1]} Bin"] = columnB
        DF[f"{columns[2]} Bin"] = columnC
        #print(DF.head(300))
        #print("Runtime: ", time.time() - x)
        return DF.to_csv('bin_csv')
        # method 1 numpy array: 
        # method 2 search: 

    def printBins(self, n=20, column="Theta"):
        lst = self.getBinBounds(n, column)
        for x in lst:
            print(x)

    # def plot2d(self, param):
    # def plot3d(self):
    # def bin(binStyle):
        # test different binning methods - papers (+ references like qubo), ML based - train on simulation data, train with cone, physics based, occupancy based
    # def binID(self, phi, chi, psi):
    # def binValue(self, binID):
    # def binValue(self, phi, chi, psi):
