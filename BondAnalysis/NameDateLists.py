import datetime
from datetime import date  
from datetime import timedelta

# Enum to easily access the relevant ISIN numbers
class ISIN:
    strISIN = "CA135087D929", "CA135087E596", "CA135087F254", "CA135087F585", \
    "CA135087G328", "CA135087ZU15", "CA135087H490", "CA135087A610", \
    "CA135087J546", "CA135087J967", "CA135087K528"
    # 

# Enum to easily access the relevant dates
class ISSUEDATE:
    dateOfIssue = datetime.date(2020,1,2), datetime.date(2020,1,3), datetime.date(2020,1,6), datetime.date(2020,1,7),\
        datetime.date(2020,1,8), datetime.date(2020,1,9), datetime.date(2020,1,10), datetime.date(2020,1,13),\
        datetime.date(2020,1,14), datetime.date(2020,1,15)