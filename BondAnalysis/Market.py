import datetime
from datetime import date  
from datetime import timedelta

from scipy.interpolate import interp1d
from scipy import interpolate

from NameDateLists import *
from AnalyticFormulas import *
from BondData import *
from Bond import *

class Market:
    bondData = BondData()
    numberOfBonds = None
    issueDate = None

    def __init__(self, issueDate):
        self.issueDate = issueDate
        isin = ISIN()
        self.numberOfBonds = len(isin.strISIN)

    def getZeroRate(self):
        zeroRate_array = []
        paymentDate_array = []
        firstBond = Bond(0, self.issueDate)
        # running_date = datetime.date(2020,9,1)
        running_date = firstBond.maturityDate
        for i in range(self.numberOfBonds):

            # Look if there is a fitting bond
            bondExists = -1
            for bondNumber in range(self.numberOfBonds):
                if self.bondData.getMaturityDate(bondNumber) == running_date:
                    bondExists = bondNumber
                    
            
            if bondExists != -1:
                # The bond exists
                bond = Bond(bondExists,self.issueDate)
                # print("Bond exists, with number: ", bondExists)
            else:
                # Bond does not exist and has to be interpolated
                # print("Bond does not exist, interpolation is used.")
                bond = Bond(None, self.issueDate, running_date)

            # print("The bond with maturity: \t" , bond.maturityDate, "has a yield of: \t", bond.getYield())


            # Calculate the zero rate of the actual period
            size = len(bond.getPayments())
            
            # Calculate the right hand side of the equation (Price-Coupon payments)
            modifiedPrice = bond.getAlternativeDirtyPrice()
            for j in range(size-1):
                # Calculate the Coupon payment and subtract it from the modified price
                individualDiscountTime = float((paymentDate_array[j] - self.issueDate).total_seconds())/(365.0*24*60*60)
                discountFactor = math.exp(-zeroRate_array[j]*individualDiscountTime)
                modifiedPrice -= bond.getPayments()[j]
            # Solve for the zero-rate    
            discountTime = float((running_date - self.issueDate).total_seconds())/(365.0*24*60*60)
            zeroRate = -math.log(modifiedPrice/bond.getPayments()[size-1])/discountTime
            # print("The zero rate at ", running_date, " is: ", zeroRate)

            # Append the zero rate to the array
            zeroRate_array.append(zeroRate)
            
            # Set the running_Date to the next coupon payment
            paymentDate_array.append(running_date)
            if running_date.month > 6:
                running_date = datetime.date(running_date.year + 1, running_date.month - 6, running_date.day)
            else:
                running_date = datetime.date(running_date.year, running_date.month + 6, running_date.day)
        
        return zeroRate_array

    def getDateArray(self):
        running_date = datetime.date(2020,3,1)
        paymentDate_array = []
        for i in range(11):
            paymentDate_array.append(running_date)
            if running_date.month > 6:
                running_date = datetime.date(running_date.year + 1, running_date.month - 6, running_date.day)
            else:
                running_date = datetime.date(running_date.year, running_date.month + 6, running_date.day)
        return paymentDate_array

    # def getForwardTimeFrame(self):
    #     forwardTimeFrame_array = []
    #     date_array = self.getDateArray()
    #     for i in range(11):
    #         if i > 3 and i%2 == 0:
    #             forwardTimeFrame_array.append( float((date_array[i]-self.issueDate).total_seconds())/(365.0*24*60*60) )
    #     return forwardTimeFrame_array

    def getForwardRate(self):
        forwardRate_array = []
        zeroRate_array = self.getZeroRate()
        date_array = self.getDateArray()
        timeFrame_array = []
        for i in range(11):
            timeFrame_array.append( float((date_array[i]-self.issueDate).total_seconds())/(365.0*24*60*60) )


        for i in range(11):
            if i > 3 and i%2 == 0:
                forwardRate_array.append(\
                    ((zeroRate_array[i]*timeFrame_array[i]) - (zeroRate_array[i-2]*timeFrame_array[i-2]))) 
                
        return forwardRate_array

