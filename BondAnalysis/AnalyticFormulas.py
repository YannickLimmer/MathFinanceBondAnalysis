import datetime
from datetime import date  
from datetime import timedelta

import math



class AnalyticFormulas:

    def yieldEquation(self, payment_array, timeToMaturity_array, price, yieldValue):
        length = len(payment_array)
        sum = 0
        for i in range(length):
            discountFactor = math.exp(-timeToMaturity_array[i]*yieldValue)
            sum += payment_array[i]*discountFactor
            # print("For ", i, " \t Discount factor ", discountFactor, " \t discountTime ", timeToMaturity_array[i])
        # print("")
        return sum - price

    def yieldDerivative(self, payment_array, timeToMaturity_array, price, yieldValue):
        length = len(payment_array)
        sum = 0
        for i in range(length):
            discountFactor = -timeToMaturity_array[i]*math.exp(-timeToMaturity_array[i]*yieldValue)
            sum += payment_array[i]*discountFactor
            print
        return sum - price
            