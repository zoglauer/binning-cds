def binnertest(df,n,epsilon,colnames=['theta','phi','scatterangle']):

  def unevenbins(df, colname, n, epsilon):
    itemsPerBin = len(df)/n
     #tolerance of 10 items diff
    # start with even bin hypothetical
    
    bins = {}
    binslist = []
    itemslist=[] #actual rows that are to be contained in these bins
    if colname =='phi':
      prev=-180
    else:
      prev = 0
    binslist.append(prev)
    for i in np.arange(n):
      keepGoing = True
      if colname =='theta' or colname =='scatterangle':
        initialcurrSize = 180/n
      elif colname=='phi':
        initialcurrSize=360/n
      iters = 0
      currSize=initialcurrSize
      while keepGoing: # bin width should start at 180/n, but starting point will be different as going across the bins.
        actualItems= df[prev < df[fullname[colname]]][df[fullname[colname]] < (prev + currSize)]
        thisbinItems = len(actualItems)
        
        if np.abs(thisbinItems - itemsPerBin) <= epsilon or iters > 1000:
          keepGoing = False
          print(prev,prev+currSize)
          bins[f'{prev} to {prev + currSize}'] = thisbinItems
          itemslist.append(actualItems)
          prev = prev + currSize
          binslist.append(prev)
          currSize = initialcurrSize # resetting this
        elif thisbinItems < itemsPerBin: # if too few items, make the bin bigger
          #  if colname =='phi':
          #   currSize=np.min([20/19*currSize, 360])
          #   if currSize == 360:
          #     bins[f'{prev} to {currSize}'] = len(df[prev < df[fullname[colname]]][df[fullname[colname]] < (currSize)])
          #     binslist.append(currSize)
          #     break
          #  else:
            currSize = np.min([20/19*currSize, 180])
            if currSize == 180:
              bins[f'{prev} to {currSize}'] = len(df[prev < df[fullname[colname]]][df[fullname[colname]] < (currSize)])
              binslist.append(currSize)
              break
          
        else: # make bin smaller
          currSize = 19/20*currSize
        iters = iters + 1
    if 180 not in binslist:
      prev = binslist[-1]
      currSize=180
      bins[f'{prev} to {currSize}'] = len(df[prev < df[fullname[colname]]][df[fullname[colname]] < (currSize)])
      binslist.append(currSize)
    return bins,binslist,itemslist

  def assigntodf(outputfromunevenbins,df,col):
    maxangle=180
    upperbounds=outputfromunevenbins[1]
    points_in_group=outputfromunevenbins[2]
    newlst = [None]*len(df) #pd.DataFrame({'a':[None]*len(df)})
    for i in np.arange(len(points_in_group)):
    #points_in_group[i][f'{col} bin']=upperbounds[i+1]
    
      if i == len(points_in_group)-1: #last box
        bound=maxangle
      else:
        bound= upperbounds[i+1]
      for j in points_in_group[i].index:
        newlst[j]= bound
    #newlst.iloc[points_in_group.index]['a']=upperbounds[i+1]
    df[f'{col} bin'] = newlst
    return df

  thetabins= unevenbins(df, 'theta', n, epsilon)
  phibins=unevenbins(df, 'phi', n, epsilon)
  scbins=unevenbins(df, 'scatterangle', n, epsilon)
  assigntodf(thetabins,df,'theta')
  assigntodf(phibins,df,'phi')
  assigntodf(scbins,df,'scatterangle')
  
  return df
