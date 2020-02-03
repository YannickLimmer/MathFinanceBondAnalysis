import csv

import datetime
from datetime import date  
from datetime import timedelta

from NameDateLists import *

# Class BondData
# - getPrice: For given MaturityDate and ISIN, the Price is retruned
# - getCoupon: For given ISIN, the Coupon is returned
# - getMaturity: For given ISIN, the Maturity is returned
class BondData:

    value_ISIN = [None]*320
    value_Coupon = [None]*320
    value_MaturityDate = [None]*320
    value_IssueDate = [None]*320
    value_Price = [None]*320

    with open('WorkingBondData.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=';')
        line_count = -1
        # MaturityDate_value = 
        for row in csv_reader:
            if line_count == -1:
                line_count += 1
            else:
                value_ISIN[line_count] = row[0]
                value_Coupon[line_count] = row[1]
                value_MaturityDate[line_count] = row[2]
                value_IssueDate[line_count] = row[3]
                value_Price[line_count] = row[4]
                line_count += 1

    
    def getPrice(self, issueDate, bondNumber):
        modifiedIssueDate = issueDate.strftime("%d.%m.%y")
        for i in range(0,320):
            if BondData.value_ISIN[i] == ISIN.strISIN[bondNumber] \
                    and BondData.value_IssueDate[i] == modifiedIssueDate:
                 return float(BondData.value_Price[i])
    
    def getCoupon(self, bondNumber):
        for i in range(0,320):
            if BondData.value_ISIN[i] == ISIN.strISIN[bondNumber]:
                 return BondData.value_Coupon[i]

    def getMaturityDate(self, bondNumber):
        for i in range(0,320):
            if BondData.value_ISIN[i] == ISIN.strISIN[bondNumber]:
                 maturityDate = BondData.value_MaturityDate[i]
                 day, month, year = map(int, maturityDate.split('.'))
                 year += 2000
                 return datetime.date(year, month, day)
