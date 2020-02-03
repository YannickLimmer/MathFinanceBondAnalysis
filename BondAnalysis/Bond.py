import datetime
from datetime import date  
from datetime import timedelta

import numpy
from scipy.interpolate import interp1d
from scipy import interpolate

from NameDateLists import *
from AnalyticFormulas import *
from BondData import *


# # Class Bond
# - Contains every payment and the corresponding payment date
# - Contains the maturity and coupon
# - Provides getMethods for each payment
# - Provides a method returning the yield
class Bond:

    bondData = BondData()
    issueDate = None
    bondNumber = None
    maturityDate = None
    coupon = None
    price = 0

    def __init__(self, bondNumber, issueDate, maturityDate = None):
        if maturityDate == None:
            self.issueDate = issueDate
            self.bondNumber = bondNumber
            self.maturityDate = self.bondData.getMaturityDate(bondNumber)
            self.coupon = float (self.bondData.getCoupon(bondNumber))
            self.price = self.bondData.getPrice(issueDate, bondNumber)
        else:
            self.issueDate = issueDate
            self.maturityDate = maturityDate

            bondFinder = 0
            isin = ISIN()
            for i in range(len(isin.strISIN)-1):
                if self.bondData.getMaturityDate(i) < maturityDate:
                    bondFinder = i
            
            # print("Interpolation between bonds.")
            # print("The maturity of the first one is: ", self.bondData.getMaturityDate(bondFinder), "\nThe maturity of the second is: ",self.bondData.getMaturityDate(bondFinder+1))
            # print("The coupon of the first one is: ", self.bondData.getCoupon(bondFinder), "\nThe coupon of the second is: ",self.bondData.getCoupon(bondFinder+1))
            # print("The price of the first one is: ", self.bondData.getPrice(issueDate, bondFinder), "\nThe price of the second is: ",self.bondData.getPrice(issueDate, bondFinder +1 ))
            ## Maybe it is best to take just an adjacent bond? 
            # Or take both bonds and interpolate the resulting zero rate?
            
            time_array = [\
                float((self.bondData.getMaturityDate(bondFinder) - self.issueDate).total_seconds())/(365.0*24*60*60),\
                float((self.bondData.getMaturityDate(bondFinder+1) - self.issueDate).total_seconds())/(365.0*24*60*60)]

            coupon_array = [self.bondData.getCoupon(bondFinder), self.bondData.getCoupon(bondFinder+1)]
            # coupon_interpolation = interp1d(time_array, coupon_array, kind = 'linear')
            coupon_interpolation = interpolate.PchipInterpolator(time_array, coupon_array)
            self.coupon = coupon_interpolation(float((maturityDate - self.issueDate).total_seconds())/(365.0*24*60*60))
            # print("The interpolated coupon is: ", self.coupon)

            price_array = [self.bondData.getPrice(issueDate, bondFinder), self.bondData.getPrice(issueDate, bondFinder+1)]
            # price_interpolation = interp1d(time_array, price_array, kind = 'linear')
            price_interpolation = interpolate.PchipInterpolator(time_array, price_array)
            self.price = price_interpolation(float((maturityDate - self.issueDate).total_seconds())/(365.0*24*60*60))
            # print("The interpolated coupon is: ", self.price)

            # print("")
        
    def getPaymentDates(self):

        paymentDate_array = []
        running_date = self.maturityDate

        while(running_date > self.issueDate):
            paymentDate_array.append(running_date)
            if running_date.month > 6:
                new_date = datetime.date(running_date.year, running_date.month - 6, running_date.day)
            else:
                new_date = datetime.date(running_date.year - 1, running_date.month + 6, running_date.day)
            running_date = new_date
        paymentDate_array.reverse()
        return paymentDate_array

    def getTimeToMaturity(self):
        paymentDate_array = self.getPaymentDates()
        timeToMaturity_array = []
        for i in range(len(paymentDate_array)):
            timeToMaturity = float((paymentDate_array[i]-self.issueDate).total_seconds())/(365.0*24*60*60)
            timeToMaturity_array.append(timeToMaturity)
        return timeToMaturity_array

    def getPayments(self):
        
        lengthOfArray = len(self.getPaymentDates())
        payment_array = [self.coupon/2]*lengthOfArray

        payment_array[lengthOfArray-1] += 100.0

        return payment_array


    def getPreviousCouponPayment(self):
        paymentDate_array = self.getPaymentDates()
        lastCouponPayment = paymentDate_array[0]
        if lastCouponPayment.month > 6:
            previousCouponPayment = datetime.date(lastCouponPayment.year, lastCouponPayment.month - 6, lastCouponPayment.day)
        else:
            previousCouponPayment = datetime.date(lastCouponPayment.year - 1, lastCouponPayment.month + 6, lastCouponPayment.day)
        return previousCouponPayment
    
    def getDirtyPrice(self):
        discountTime = float((self.issueDate-self.getPreviousCouponPayment()).total_seconds())/(365.0*24*60*60)
        # print("The clean price is" , self.price)
        # print("The dirty price is" , self.price + discountTime*self.coupon)
        return self.price + discountTime*self.coupon

    def getAlternativeDirtyPrice(self):
      # First, we calculate the yield for issueDate: lastPayment
      # We can use the clean price, since it equals the dirty price
        # We set up the payment and time arrays
        # # payment_array remains the same
        payment_array = self.getPayments()
        # # timeToMatuirty_array is modified
        paymentDate_array = self.getPaymentDates()
        timeToMaturity_array = []
        for i in range(len(paymentDate_array)):
            timeToMaturity = float((paymentDate_array[i]-self.getPreviousCouponPayment()).total_seconds())/(365.0*24*60*60)
            timeToMaturity_array.append(timeToMaturity)

        analyticFormulas = AnalyticFormulas()
        yieldValue = 1.0
        yieldValue_new = 0.1
        while abs(yieldValue - yieldValue_new) > 100*numpy.finfo(float).eps:
            yieldValue = yieldValue_new
            yieldValue_new = yieldValue - \
                analyticFormulas.yieldEquation(payment_array, timeToMaturity_array, self.price, yieldValue)/ \
                    analyticFormulas.yieldDerivative(payment_array, timeToMaturity_array, self.price, yieldValue)
        
        #Calculate the 'Par Coupon'
        discountSum = 0
        for i in range(len(paymentDate_array)):
            discountSum += math.exp(-timeToMaturity_array[i]*yieldValue_new)
        parCoupon = (100.0-100.0*math.exp(-timeToMaturity_array[len(paymentDate_array)-1]*yieldValue_new))\
            /discountSum
        # We use this yield, instead of the coupon to calculate the accrued interest.
        discountTime = float((self.issueDate-self.getPreviousCouponPayment()).total_seconds())/(365.0*24*60*60)

        return self.price + discountTime*parCoupon*2

    def getYield(self):
        timeToMaturity_array = self.getTimeToMaturity()
        payment_array = self.getPayments()

        price = self.getAlternativeDirtyPrice() ###
        analyticFormulas = AnalyticFormulas()
        yieldValue = 1.0
        yieldValue_new = 0.1
        while abs(yieldValue - yieldValue_new) > 100*numpy.finfo(float).eps:
            yieldValue = yieldValue_new
            yieldValue_new = yieldValue - \
                analyticFormulas.yieldEquation(payment_array, timeToMaturity_array, price, yieldValue)/ \
                    analyticFormulas.yieldDerivative(payment_array, timeToMaturity_array, price, yieldValue)
        
        
        # yieldValue_new = self.getAlternativeDirtyPrice()
        # print("The yield is: ", yieldValue_new, "\t the alternative yield is: ", self.getAlternativeDirtyPrice())
        return  yieldValue_new


