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
        # print(self.df.head())
        # print("Method 2", time.time() - self.start)

        # for data set "/volumes/selene/users/andreas/simulationScript/Output/TestSource.926.inc1.id1.tra.gz.pkl",
        # Method 1 took 71.73062920570374 seconds and Method 2 took 15.090354919433594
    
    def bin(self, n=20, column="Theta"):
        x = time.time()
        self.bins[f"{column} {n}"] = []
        print(self.df.head(30))
        currDf = self.df.sort_values(by=column).reset_index(drop=False)
        l = len(currDf) / 2
        print(currDf.loc[[l - 10]])
        print(currDf.loc[[l - 9]])
        print(currDf.loc[[l - 8]])
        print(currDf.loc[[l - 7]])
        print(currDf.loc[[l - 6]])
        print(currDf.loc[[l - 5]])
        print(currDf.loc[[l - 4]])
        print(currDf.loc[[l - 3]])
        print(currDf.loc[[l - 2]])
        print(currDf.loc[[l - 1]])
        print(currDf.loc[[l]])
        print(currDf.loc[[l + 1]])
        print(currDf.loc[[l + 2]])
        print(currDf.loc[[l + 3]])
        print(currDf.loc[[l + 4]])
        print(currDf.loc[[l + 5]])
        print(currDf.loc[[l + 6]])
        print(currDf.loc[[l + 7]])
        print(currDf.loc[[l + 8]])
        print(currDf.loc[[l + 9]])
        print(currDf.loc[[l + 10]])
        # print(currDf.head())
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
        print("Bin Runtime:", time.time() - x)
            

    def showBins(self, n=20, column="Theta"):
        x = time.time()
        theBin = self.bins[f"{column} {n}"]
        for x in theBin:
            stri = "["
            stri += str(list(x["Theta"])[0])
            stri += ", "
            stri += str(list(x["Theta"])[-1])
            stri += "]"
            print(stri)
        print("Show Bins Runtime:", time.time() - x)

    # def binTrial(self, n, col="Scatter Angle"):
    #     self.mergeSort(col)
    #     dataPoints = len(self.df)
    #     size = dataPoints // n
    #     numOverflow = 0
    #     numBins = 0
    #     binPos = 0
    #     overflow = dataPoints - n * size
    #     self.bins = [[None]] * n
    #     for i in range(len(dataPoints)):
    #         if (binPos < size):
    #             self.bins[numBins].append(i)
    #             binPos += 1
    #         elif (binPos == size and overflow < overflow):
    #             self.bins[numBins].append(i)
    #             numOverflow += 1
    #             binPos += 1
    #         else:
    #             numBins += 1
    #             binPos = 0
    #             self.bins[numBins].append(i)

    # def mergeSort(self, col):
    #     if 

    # def merge(first, second):
    
    # def binnertest(self, df, n, epsilon, colnames=['theta','phi','scatterangle']):
    #     def unevenbins(df, colname, n, epsilon):
    #         itemsPerBin = len(df) / n
    #         # tolerance of 10 items diff
    #         # start with even bin hypothetical
            
    #         bins = {}
    #         binslist = []
    #         itemslist = [] # actual rows that are to be contained in these bins
    #         if colname == 'phi':
    #             prev = -180
    #         else:
    #             prev = 0
    #         binslist.append(prev)
    #         for i in range(n):
    #             keepGoing = True
    #             if colname == 'theta' or colname == 'scatterangle':
    #                 initialcurrSize = 180 / n
    #             elif colname == 'phi':
    #                 initialcurrSize = 360 / n
    #             iters = 0
    #             currSize = initialcurrSize
    #             fullname = {'theta': 'Theta (Polar Angle)', 'phi': 'Phi (Azimuthal)', 'scatterangle': 'Scatter Angle'}
    #             while keepGoing: # bin width should start at 180/n, but starting point will be different as going across the bins.
    #                 actualItems= df[prev < df[fullname[colname]]][df[fullname[colname]] < (prev + currSize)]
    #                 thisbinItems = len(actualItems)

    #                 x = (time.time() - self.start) // 1
    #                 if x % 10 == 0:
    #                     print("Still going, time elapsed:", x, "seconds")

    #                 if np.abs(thisbinItems - itemsPerBin) <= epsilon or iters > 1000:
    #                     keepGoing = False
    #                     print(prev, prev + currSize)
    #                     bins[f'{prev} to {prev + currSize}'] = thisbinItems
    #                     itemslist.append(actualItems)
    #                     prev = prev + currSize
    #                     binslist.append(prev)
    #                     currSize = initialcurrSize # resetting this
    #                 elif thisbinItems < itemsPerBin:
    #                     currSize = min([20/19*currSize, 180])
    #                     if currSize == 180:
    #                         bins[f'{prev} to {currSize}'] = len(df[prev < df[fullname[colname]]][df[fullname[colname]] < (currSize)])
    #                         binslist.append(currSize)
    #                         break
                    
    #                 else: # make bin smaller
    #                     currSize = 19 / 20 * currSize
    #                 iters += 1
    #             if 180 not in binslist:
    #                 prev = binslist[-1]
    #                 currSize = 180
    #                 bins[f'{prev} to {currSize}'] = len(df[prev < df[fullname[colname]]][df[fullname[colname]] < (currSize)])
    #                 binslist.append(currSize)
    #             return bins, binslist, itemslist

    #     def assigntodf(outputfromunevenbins, df, col):
    #         maxangle = 180
    #         upperbounds = outputfromunevenbins[1]
    #         points_in_group = outputfromunevenbins[2]
    #         newlst = [None] * len(df)
    #         for i in range(len(points_in_group)):
    #             if i == len(points_in_group)-1: # last box
    #                 bound = maxangle
    #             else:
    #                 bound = upperbounds[i+1]
    #             for j in points_in_group[i].index:
    #                 newlst[j]= bound
    #         df[f'{col} bin'] = newlst
    #         return df

    #     thetabins = unevenbins(df, 'theta', n, epsilon)
    #     phibins = unevenbins(df, 'phi', n, epsilon)
    #     scbins = unevenbins(df, 'scatterangle', n, epsilon)
    #     assigntodf(thetabins, df, 'theta')
    #     assigntodf(phibins, df, 'phi')
    #     assigntodf(scbins, df, 'scatterangle')
        
    #     return df

    # def plot2d(self, param):
    # def plot3d(self):
    # def bin(binStyle):
        # test different binning methods - papers (+ references like qubo), ML based - train on simulation data, train with cone, physics based, occupancy based
    # def binID(self, phi, chi, psi):
    # def binValue(self, binID):
    # def binValue(self, phi, chi, psi):
