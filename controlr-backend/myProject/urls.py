"""myProject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from webapp.views import *

import logging
logging.basicConfig(level="DEBUG")

urlpatterns = [
    path('admin/',admin.site.urls),
    path('buildings/',buildingsList.as_view()),# GET - to get the entire building, room, device info in hierarchy
    path('buildings/<int:id>',buildingsListDetailedView.as_view()),#  GET -to get the specific building info eg: localhost:8000/buildings/1
    path('rooms/',roomsList.as_view()),#  GET -to get the entire room, device info in hierarchy
    path('rooms/<int:id>',roomsListDetailedView.as_view()),#  GET -to get the specific room info eg : localhost:8000/rooms/1
    path('devices/',devicesList.as_view()),#  GET -to get the list of all devices
    path('devices/<int:id>',devicesListDetailedView.as_view()),#  GET -to get specific device eg : localhost:8000/devices/1
    path('loggings/',loggingList.as_view()),# GET- to get the logging info AND POST- to add logs eg: {device=1, state = "false"}
    path('loggingfilter/',loggingfilter.as_view()),#  GET -to filter in logging using Eg: (localhost:8000/loggingfilter/?device_id=val&created_at=val&created_at__lte=val&created_at__gte=val) can also leave any unwantted parameter
    path('hardware/',hardwareDevicesList.as_view()), #hardware hit to get data
    path('schedule/',ScheduleTrigger.as_view()), #UTC_time and trigger time is in cron type --- POST { "device_id" : 11000001 , "state" : false, "trigger_time" : "28 9 * * *" }
    path('schedule/<str:id>',scheduleTriggerDetailedView.as_view()),  # use DELETE - http://localhost:8000/schedule/<schedule_id> eg:http://localhost:8000/schedule/7f9769a2-d887-484f-9dbc-be2e34fbf293
    path('hours/',WeekWise.as_view()), # POST - send a post command eg:{ "device" : 2, "start_date" : "2020-03-15", "end_date" : "2020-03-21" }


 ]
