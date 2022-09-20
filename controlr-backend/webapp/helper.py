import datetime
from .serializers import *
from pytz import timezone
from croniter import *
"""To fetch the total ON Time of the device"""
def hourCalc(data_set, date_min, date_max):

    min = date_min
    max = date_max
    hrs = date_min
    state = None

    for x in data_set:
        # hrs = datetime.strptime(x["created_at"],'%Y-%m-%dT%H:%M:%S.%f')
        if (state != x["state"]) and (x["state"] == False):
            time_var = datetime.strptime(x["created_at"],'%Y-%m-%dT%H:%M:%S.%f') #from here want to get time
            hrs += time_var - min
            state = False

        elif (state != x["state"]) and (x["state"] == True):
            min = datetime.strptime(x["created_at"],'%Y-%m-%dT%H:%M:%S.%f') #from here want to get time
            state = True

    if (state == True):
         hrs += max - min
    return hrs
def dayWise(dev_id, start_date, end_date):

    start_date_parse = datetime.strptime(start_date,'%Y-%m-%d')
    end_date_parse = datetime.strptime(end_date,'%Y-%m-%d')
    i = (end_date_parse.day-start_date_parse.day)
    myList=[]
    watt_hour = start_date_parse-start_date_parse
    ret = []
    for x in range(i+1):
        queryset = Logging.objects.filter(created_at__date=datetime(start_date_parse.year, start_date_parse.month, start_date_parse.day+x)).filter(device=dev_id)
        serializer = loggingSerializer(queryset, many=True)
        t = hourCalc(serializer.data, datetime(start_date_parse.year, start_date_parse.month, start_date_parse.day+x), datetime(start_date_parse.year, start_date_parse.month, start_date_parse.day+x,23,59,59))
        watt_hour = watt_hour+(t- datetime(start_date_parse.year, start_date_parse.month, start_date_parse.day+x))
        temp = t.strftime("%Y-%m-%dT%H:%M:%S")
        myList.append(temp)
        #return watt_hour/(3600)
    ret.append(myList)
    ret.append(watt_hour/(3600))
    return ret

""" cron object local to utc conversion"""
def toUtc():
    test = "10 1 * * *"
    cron_Parse = datetime.strptime(test,"%M %H %d %m %w")
    cron_Parse_Utc = cron_Parse.replace(tzinfo=timezone('UTC'))
    cron_Parse_Utc_String = cron_Parse_Utc.strftime("%M %H %d %m %w")
    return cron_Parse_Utc_String
