import datetime
from datetime import date  
from datetime import timedelta


import math
import numpy as np
from matplotlib import pyplot as plt
from scipy.interpolate import interp1d
from scipy import interpolate


from NameDateLists import *
from AnalyticFormulas import *
from BondData import *
from Bond import *
from Market import *
from Covariance import *


ORIGINALYIELD = False
YIELD = False
ZERO = False
FORWARD = False
EXAMPLE = False
COVYIELD = True
COVFORWARD = True

#%%
if YIELD:
    interpolateGraph = True
    issueDate = ISSUEDATE()
    numberOfBonds = 11
    plt.figure(0)
    for i in range(10):
        yieldForDate_array = []
        timeForDate_array = []
        for j in range(numberOfBonds):
            bond = Bond(j, issueDate.dateOfIssue[i])
            yieldForDate_array.append(bond.getYield())
            timeForDate_array.append(float((bond.maturityDate-bond.issueDate).total_seconds())/(365.0*24*60*60))  
            print("The bond with maturity: \t" , bond.maturityDate, "has a yield of: \t", bond.getYield())

        if interpolateGraph:
            x = np.linspace(timeForDate_array[len(timeForDate_array)-1], timeForDate_array[0], num=101, endpoint=True) #timeForDate_array[0]
            # interpolatedValues = interp1d(timeForDate_array, yieldForDate_array, kind = 'cubic')
            interpolatedValues = interpolate.PchipInterpolator(timeForDate_array, yieldForDate_array)
            plt.plot(x, 100*interpolatedValues(x), label = issueDate.dateOfIssue[i], linewidth = 0.6) 
        else: 
            plt.plot(timeForDate_array, yieldForDate_array, label = issueDate.dateOfIssue[i], linewidth = 0.6)

    plt.legend()
    plt.xlabel('Time in Years', fontsize=12)
    plt.ylabel('Yield in %', fontsize=12)
    plt.ylim(1, 2)
    plt.show()

# %%
if ZERO:
    issueDate = ISSUEDATE()
    numberOfBonds = 11
    plt.figure(1)
    for tradingDay in issueDate.dateOfIssue:
        market = Market(tradingDay)

        timeForDate_array = []
        for j in range(numberOfBonds):
            timeForDate_array.append(float((market.getTimeFrame()[j]-tradingDay).total_seconds())/(365.0*24*60*60))  
        
        # interpolatedValues = interp1d(timeForDate_array, market.getZeroRate(), kind='cubic')
        zeroRate_array = market.getZeroRate()
        interpolatedValues = interpolate.PchipInterpolator(timeForDate_array, zeroRate_array)
        x = np.linspace(timeForDate_array[0], timeForDate_array[numberOfBonds-1], num=101, endpoint=True) #timeForDate_array[0]

        plt.plot(x, 100*interpolatedValues(x) , label = tradingDay, linewidth = 0.6)
    plt.legend()
    plt.xlabel('Time in Years', fontsize=12)
    plt.ylabel('Zero Rate in %', fontsize=12)
    plt.ylim(1, 2)
    plt.show()

#%%
if FORWARD:
    issueDate = ISSUEDATE()
    plt.figure(2)
    for tradingDay in issueDate.dateOfIssue:
        market = Market(tradingDay)
        timeSpan = []
        for i in range(11):
            if i>3 and i%2 == 0:
                timeSpan.append( (market.getDateArray()[i]-tradingDay).total_seconds()/(365.0*24*60*60) )
        value_array = market.getForwardRate()

        x = np.linspace(timeSpan[0], timeSpan[-1], num=101, endpoint=True)
        # interpolatedValues = interp1d(timeSpan, value_array, kind='cubic')
        interpolatedValues = interpolate.PchipInterpolator(timeSpan, value_array)
        plt.plot(x , 100*interpolatedValues(x), label = tradingDay, linewidth = 0.6)
    plt.legend()
    plt.xlabel('Time in Years', fontsize=12)
    plt.ylabel('Forward Rate in %', fontsize=12)
    plt.show()

    print("Executed")

#%%
if EXAMPLE:
    array_1 = [4.0, 4.2, 3.9, 4.3, 4.1]
    array_2 = [2.0 ,2.1 ,2.0, 2.1, 2.2]
    array_3 = [0.6, 0.59, 0.58, 0.62, 0.63]
    array = [array_1, array_2, array_3]
    covariance = Covariance(array)
    print(covariance.matrix[0,0], "\t", covariance.matrix[0,1], "\t", covariance.matrix[0,2])
    print(covariance.matrix[1,0], "\t", covariance.matrix[1,1], "\t", covariance.matrix[1,2])
    print(covariance.matrix[2,0], "\t", covariance.matrix[2,1], "\t", covariance.matrix[2,2])

#%% 
if COVYIELD:
    sampleData = []
    selectedBond_array = [2,4,6,8,10]
    issueDate = ISSUEDATE()
    for bondNumber in selectedBond_array:
        sampleDataForBond = []
        for i in range(9):
            bond1 = Bond(bondNumber, issueDate.dateOfIssue[i])
            bond2 = Bond(bondNumber, issueDate.dateOfIssue[i+1])
            sampleDataForBond.append(math.log(bond2.getYield()/bond1.getYield()))
            # if bondNumber == 2 or bondNumber == 4:
            #     print(bond.getYield())
        sampleData.append(sampleDataForBond)
        # print()
    covariance = Covariance(sampleData)
    print(" %1.6f & %1.6f & %1.6f & %1.6f & %1.6f \\\\"  % (covariance.matrix[0,0], covariance.matrix[0,1], covariance.matrix[0,2], covariance.matrix[0,3], covariance.matrix[0,4]))
    print(" %1.6f & %1.6f & %1.6f & %1.6f & %1.6f \\\\"  % (covariance.matrix[1,0], covariance.matrix[1,1], covariance.matrix[1,2], covariance.matrix[1,3], covariance.matrix[1,4]))
    print(" %1.6f & %1.6f & %1.6f & %1.6f & %1.6f \\\\"  % (covariance.matrix[2,0], covariance.matrix[2,1], covariance.matrix[2,2], covariance.matrix[2,3], covariance.matrix[2,4]))
    print(" %1.6f & %1.6f & %1.6f & %1.6f & %1.6f \\\\"  % (covariance.matrix[3,0], covariance.matrix[3,1], covariance.matrix[3,2], covariance.matrix[3,3], covariance.matrix[3,4]))
    print(" %1.6f & %1.6f & %1.6f & %1.6f & %1.6f \\\\"  % (covariance.matrix[4,0], covariance.matrix[4,1], covariance.matrix[4,2], covariance.matrix[4,3], covariance.matrix[4,4]))

    print()

    print(covariance.eigenValue_array)

    print()
    print(covariance.eigenVector_matrix)
    print()

    print(" %1.6f & %1.6f & %1.6f & %1.6f & %1.6f \\\\"  % (covariance.eigenValue_array[0], covariance.eigenValue_array[1], covariance.eigenValue_array[2], covariance.eigenValue_array[3], covariance.eigenValue_array[4]))

    for i in range(5):
        print(" v_%1d = \\left( \\begin{array}{r} %1.6f \\\\ %1.6f \\\\ %1.6f \\\\ %1.6f \\\\ %1.6f \\end{array} \\right)"  % (i+1, covariance.eigenVector_matrix[0,i], covariance.eigenVector_matrix[1,i],covariance.eigenVector_matrix[2,i],covariance.eigenVector_matrix[3,i],covariance.eigenVector_matrix[4,i]))

    print()


#%% 
if COVFORWARD:
    sampleData = []
    issueDate = ISSUEDATE()

    for t in range(4):
        sampleDataForBond = []
        for i in range(9):
            market1 = Market(issueDate.dateOfIssue[i])
            market2 = Market(issueDate.dateOfIssue[i+1])
            sampleDataForBond.append(math.log(market2.getForwardRate()[t]/market1.getForwardRate()[t] ) )
        sampleData.append(sampleDataForBond)
    covariance = Covariance(sampleData)
    print(" % 1.6f & % 1.6f & % 1.6f & % 1.6f \\\\" % (covariance.matrix[0,0], covariance.matrix[0,1], covariance.matrix[0,2], covariance.matrix[0,3]))
    print(" % 1.6f & % 1.6f & % 1.6f & % 1.6f \\\\" % (covariance.matrix[1,0], covariance.matrix[1,1], covariance.matrix[1,2], covariance.matrix[1,3]))
    print(" % 1.6f & % 1.6f & % 1.6f & % 1.6f \\\\" % (covariance.matrix[2,0], covariance.matrix[2,1], covariance.matrix[2,2], covariance.matrix[2,3]))
    print(" % 1.6f & % 1.6f & % 1.6f & % 1.6f \\\\" % (covariance.matrix[3,0], covariance.matrix[3,1], covariance.matrix[3,2], covariance.matrix[3,3]))

    print()

    print(covariance.eigenValue_array)
    print()
    print(covariance.eigenVector_matrix)
    print()
    print(" %1.6f & %1.6f & %1.6f & %1.6f \\\\"  % (covariance.eigenValue_array[0], covariance.eigenValue_array[1], covariance.eigenValue_array[2], covariance.eigenValue_array[3]))

    for i in range(4):
        print(" v_%1d = \\left( \\begin{array}{r} %1.6f \\\\ %1.6f \\\\ %1.6f \\\\ %1.6f \\end{array} \\right)"  % (i+1, covariance.eigenVector_matrix[0,i], covariance.eigenVector_matrix[1,i],covariance.eigenVector_matrix[2,i],covariance.eigenVector_matrix[3,i]))

    print()



#%%
if ORIGINALYIELD:
    yield_array = [0.0167153000, 0.0172620000, 0.0174773000, 0.0176927000, 0.0172551000, 0.0171428000, 0.0170454000, 0.0169654000, 0.0169023000, 0.0168548000, 0.0168209000, 0.0167987000, 0.0167862000, 0.0167819000, 0.0167841000, 0.0167915000, 0.0168031000, 0.0168178000, 0.0168349000, 0.0168536000]
    x = [0.25, 0.5, 0.75, 1.0, 1.25, 1.5, 1.75, 2.0, 2.25, 2.5, 2.75, 3.0, 3.25, 3.5, 3.75, 4.0, 4.25, 4.5, 4.75, 5.0,]
    plt.plot(x, yield_array, linewidth = 0.6) 
    plt.xlabel('Time', fontsize=12)
    plt.ylabel('Yield', fontsize=12)
    plt.show()
