from django.shortcuts import render
import datetime
from datetime import datetime
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from rest_framework.generics import ListAPIView
from rest_framework.views import *
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import generics
from .models import *
from .serializers import *
from django_filters import rest_framework as filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import *
from .schedule import *
from .helper import *

class loggingFilter(filters.FilterSet):
    device_id = filters.CharFilter('device__device_id')

    class Meta:
        model = Logging
        fields = {
            'device_id': ['exact'],
            'created_at': ['date', 'lte', 'gte']
        }


class loggingfilter(generics.ListAPIView):
    queryset = Logging.objects.all()
    serializer_class = loggingSerializer
    filter_backends = (DjangoFilterBackend,)
    filter_class = loggingFilter


class loggingList(APIView):

    def get(self, request):
        devices1 = Logging.objects.all()
        serializer = loggingSerializer(devices1, many=True)
        return Response(serializer.data)

    def post(self, request):
        data = request.data
        serializer = loggingAdd(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.erros, status=400)


class hardwareDevicesList(APIView):
    def get_object(self, id):
        try:
            return Logging.objects.all().filter(device=id).order_by('-created_at')[:1]

        except Devices.DoesNotExist as e:
            return Response({"error": "Given question object not found."}, status=404)

    def get(self, request):

        queryset = Devices.objects.none()
        val = Devices.objects.values_list('id', flat=True).order_by('id')
        for x in val:
            instance = self.get_object(x)
            queryset |= instance
        serializer = hardwareSerializer(queryset, many=True)
        return Response(serializer.data)


class devicesList(APIView):

    def get(self, request):
        devices1 = Devices.objects.all()
        serializer = devicesSerializer(devices1, many=True)
        return Response(serializer.data)

    def post(self, request):
        data = request.data
        serializer = devicesSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.erros, status=400)


class devicesListDetailedView(APIView):
    def get_object(self, id):
        try:
            return Devices.objects.get(id=id)
        except Devices.DoesNotExist as e:
            return Response({"error": "Given question object not found."}, status=404)

    def get(self, request, id=None):
        instance = self.get_object(id)
        serializer = devicesSerializer(instance)
        return Response(serializer.data)

    def put(self, request, id=None):
        data = request.data
        instance = self.get_object(id)
        serializer = devicesSerializer(instance, data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=200)
        return Response(serializer.erros, status=400)

    def delete(self, request, id=None):
        instance = self.get_object(id)
        instance.delete()
        return HttpResponse(status=204)


class buildingsList(APIView):

    def get(self, request):
        devices1 = Buildings.objects.all()
        serializer = buildingsSerializerHierarchy(devices1, many=True)
        return Response(serializer.data)

    def post(self, request):
        data = request.data
        serializer = buildingsSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.erros, status=400)
class buildingsListDetailedView(APIView):
    def get_object(self, id):
        try:
            return Buildings.objects.get(id=id)
        except Buildings.DoesNotExist as e:
            return Response({"error": "Given question object not found."}, status=404)

    def get(self, request, id=None):
        instance = self.get_object(id)
        serializer = buildingsSerializer(instance)
        return Response(serializer.data)

    def put(self, request, id=None):
        data = request.data
        instance = self.get_object(id)
        serializer = buildingsSerializer(instance, data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=200)
        return Response(serializer.erros, status=400)

    def delete(self, request, id=None):
        instance = self.get_object(id)
        instance.delete()
        return HttpResponse(status=204)


class roomsList(APIView):

    def get(self, request):
        devices1 = Rooms.objects.all()
        serializer = roomsSerializerHierarchy(devices1, many=True)
        return Response(serializer.data)

    def post(self, request):
        data = request.data
        serializer = roomsSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.erros, status=400)
class roomsListDetailedView(APIView):
    def get_object(self, id):
        try:
            return Rooms.objects.get(id=id)
        except Rooms.DoesNotExist as e:
            return Response({"error": "Given question object not found."}, status=404)

    def get(self, request, id=None):
        instance = self.get_object(id)
        serializer = roomsSerializer(instance)
        return Response(serializer.data)

    def put(self, request, id=None):
        data = request.data
        instance = self.get_object(id)
        serializer = roomsSerializer(instance, data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=200)
        return Response(serializer.erros, status=400)

    def delete(self, request, id=None):
        instance = self.get_object(id)
        instance.delete()
        return HttpResponse(status=204)



class ScheduleTrigger(APIView):
    """schedule"""

    def get(self, request):
        res = view_schedule()
        return Response(res)

    def post(self, request):
        data = request.data
        dev_id = data["device_id"]
        dev_state = data["state"]
        dev_time = data["trigger_time"]
        run_schedule(dev_id, dev_state, dev_time)

        return Response(f"Schedule of Device Id = {dev_id} at Time = {dev_time} with State = {dev_state} is Created")
class scheduleTriggerDetailedView(APIView):

    def delete(self, request, id=None):
        res_deleted = schedule_delete(id)
        return HttpResponse(res_deleted, status=204)




class WeekWise(APIView):

    def post(self, request):
        data = request.data
        start_date = data["start_date"]
        end_date = data["end_date"]
        dev_id = data["device"]
        myList = dayWise(dev_id, start_date, end_date)
        res = Devices.objects.all().filter(id=dev_id)
        serializer = devicesSerializer(res, many=True)
        watt = serializer.data[0]["watts_rating"]
        watt_used = watt*myList[1]
        dic = {}
        dic.update({"usage" : myList[0]})
        dic.update({"watts": watt})
        dic.update({"total_hours": myList[1]})
        dic.update({"watt_hour": watt_used})
        dic.update({"unit" : watt_used/1000})

        return Response(dic)
