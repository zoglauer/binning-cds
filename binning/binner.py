import os
import pandas as pd
import numpy as np
import pickle
import time

class Binner():
    def __init__(self, dataFile):
        # start times for runtime analysis
        self.start = time.time()
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
            dataI = []
            dataI.append(self.lst[0][i])
            dataI.append(self.lst[1][i])
            dataI.append(self.lst[2][i])
            dataI.append(self.lst[3][i])
            dataI.append(self.lst[4][i])
            dataI.append(self.lst[5][i])
            data.append(dataI)
        self.df = pd.DataFrame(data, columns={0: "Event ID", 1: "Energy", 2: "Theta", 3: "Phi", 4: "Scatter Angle", 5: "Path Length"})
        # RUNTIME TEST
        # print(self.df.head())
        # print("Method 2", time.time() - self.start)

        # for data set "/volumes/selene/users/andreas/simulationScript/Output/TestSource.926.inc1.id1.tra.gz.pkl",
        # Method 1 took 71.73062920570374 seconds and Method 2 took 15.090354919433594
    
import os
import pandas as pd
import numpy as np
import pickle

class Binner():
    def __init__(self):
        self.x = 0
        # ending = os.path.splitext(dataFile)[-1].lower()
        # print(dataFile)
        # if ending == ".pkl":
        #     self.df = pd.read_pickle(dataFile)
        # else:
        #     self.df = pd.read_csv(dataFile)
    # def bin(binStyle):
        # test different binning methods - papers (+ references like qubo), ML based - train on simulation data, train with cone, physics based, occupancy based
    # def binID(self, phi, chi, psi):
    # def binValue(self, binID):
    # def binValue(self, phi, chi, psi):
 
    def filesplit(self, filepath = "/volumes/selene/users/andreas/simulationScript/Output/TestSource.926.inc1.id1.tra.gz.pkl"):
        fil = open(filepath, "rb")
        # unpickled = pickle.load(fil)
        
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
    
    def binnertest(self, df, n, epsilon, colnames=['theta','phi','scatterangle']):
        def unevenbins(df, colname, n, epsilon):
            itemsPerBin = len(df) / n
            # tolerance of 10 items diff
            # start with even bin hypothetical
            
            bins = {}
            binslist = []
            itemslist = [] # actual rows that are to be contained in these bins
            if colname == 'phi':
                prev = -180
            else:
                prev = 0
            binslist.append(prev)
            for i in range(n):
                keepGoing = True
                if colname == 'theta' or colname == 'scatterangle':
                    initialcurrSize = 180 / n
                elif colname == 'phi':
                    initialcurrSize = 360 / n
                iters = 0
                currSize = initialcurrSize
                fullname = {'theta': 'Theta (Polar Angle)', 'phi': 'Phi (Azimuthal)', 'scatterangle': 'Scatter Angle'}
                while keepGoing: # bin width should start at 180/n, but starting point will be different as going across the bins.
                    actualItems= df[prev < df[fullname[colname]]][df[fullname[colname]] < (prev + currSize)]
                    thisbinItems = len(actualItems)
                
                    if np.abs(thisbinItems - itemsPerBin) <= epsilon or iters > 1000:
                        keepGoing = False
                        print(prev, prev + currSize)
                        bins[f'{prev} to {prev + currSize}'] = thisbinItems
                        itemslist.append(actualItems)
                        prev = prev + currSize
                        binslist.append(prev)
                        currSize = initialcurrSize # resetting this
                    elif thisbinItems < itemsPerBin:
                        currSize = min([20/19*currSize, 180])
                        if currSize == 180:
                            bins[f'{prev} to {currSize}'] = len(df[prev < df[fullname[colname]]][df[fullname[colname]] < (currSize)])
                            binslist.append(currSize)
                            break
                    
                    else: # make bin smaller
                        currSize = 19 / 20 * currSize
                    iters += 1
                if 180 not in binslist:
                    prev = binslist[-1]
                    currSize = 180
                    bins[f'{prev} to {currSize}'] = len(df[prev < df[fullname[colname]]][df[fullname[colname]] < (currSize)])
                    binslist.append(currSize)
                return bins, binslist, itemslist

        def assigntodf(outputfromunevenbins, df, col):
            maxangle = 180
            upperbounds = outputfromunevenbins[1]
            points_in_group = outputfromunevenbins[2]
            newlst = [None] * len(df)
            for i in range(len(points_in_group)):
                if i == len(points_in_group)-1: # last box
                    bound = maxangle
                else:
                    bound = upperbounds[i+1]
                for j in points_in_group[i].index:
                    newlst[j]= bound
            df[f'{col} bin'] = newlst
            return df

        thetabins = unevenbins(df, 'theta', n, epsilon)
        phibins = unevenbins(df, 'phi', n, epsilon)
        scbins = unevenbins(df, 'scatterangle', n, epsilon)
        assigntodf(thetabins, df, 'theta')
        assigntodf(phibins, df, 'phi')
        assigntodf(scbins, df, 'scatterangle')
        
        return df

    # def plot2d(self, param):
    # def plot3d(self):

    # def plot2d(self, param):
    # def plot3d(self):
    # def bin(binStyle):
        # test different binning methods - papers (+ references like qubo), ML based - train on simulation data, train with cone, physics based, occupancy based
    # def binID(self, phi, chi, psi):
    # def binValue(self, binID):
    # def binValue(self, phi, chi, psi):
