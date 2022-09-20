
"""import schedule
import time
from .models import *
from django_rq import job
from .serializers import *

def create_log(dev_id, dev_state):
    i = Devices.objects.get(device_id=dev_id)
    Logging.objects.create(device=i, state=dev_state)

@job('default')
def run_schedule():
    obj = Schedules.objects.all()
    serializer = scheduleSerializer(obj, many=True)
    for x in serializer.data:
        schedule.every().day.at(x["trigger_time"]).do(create_log, x["device_id"],x["device_state"])

    while True:
        schedule.run_pending()
        time.sleep(10)"""
from redis import Redis
from rq import Queue
from rq_scheduler import Scheduler
from datetime import timedelta
from .models import *

############################################################
def create_log(dev_ids, dev_state):

    i = Devices.objects.get(device_id=dev_ids)
    Logging.objects.create(device=i, state=dev_state)


def run_schedule(dev_id, dev_state, dev_time):
    # import ipdb
    # ipdb.set_trace()
    scheduler = Scheduler(connection=Redis())  # Get a scheduler for the "default" queue

    scheduler.cron(
    dev_time,                # A cron string (e.g. "0 0 * * 0")
    func=create_log,                  # Function to be queued
    args=[dev_id, dev_state],
    repeat=None,                  # Repeat this number of times (None means repeat forever)

)
    return dev_id

##################################################################
def view_schedule():
    scheduler = Scheduler(connection=Redis())  # Get a scheduler for the "default" queue
    l = scheduler.get_jobs(with_times=True)
    data_list = []
    for x in l:
        aa={}
        a,b = x
        aa.update({"schedule_id" : a._id})
        aa.update({"time" : b})
        aa.update({"device_id" : a.args[0]})
        aa.update({"state" : a.args[1]})
        data_list.append(aa)
    return data_list
####################################################################
def schedule_delete(schedule_inst):
    scheduler = Scheduler(connection=Redis())  # Get a scheduler for the "default" queue
    scheduler.cancel(schedule_inst)
    return "Deleted"
#####################################################################

