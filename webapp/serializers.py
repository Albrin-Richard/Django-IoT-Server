from rest_framework import serializers
from .models import *

class loggingSerializer(serializers.ModelSerializer):
    device_id = serializers.ReadOnlyField(source='device.device_id')
    device_name = serializers.ReadOnlyField(source='device.device_name')
    device_type = serializers.ReadOnlyField(source='device.device_type')
    class Meta:
         model = Logging
         fields = [
             "device",
             "device_id",
             "state",
             "device_name",
             "device_type",
             "created_at"

         ]
class loggingAdd(serializers.ModelSerializer):
    class Meta:
        model = Logging
        fields = "__all__"

class devicesSerializer(serializers.ModelSerializer):
    #entry = loggingSerializer(many=True)


    class Meta:
         model = Devices
         fields = "__all__"


class hardwareSerializer(serializers.ModelSerializer):
    device_id = serializers.ReadOnlyField(source='device.device_id')
    device_name = serializers.ReadOnlyField(source='device.device_name')
    device_type = serializers.ReadOnlyField(source='device.device_type')
    class Meta:
         model = Logging
         fields = [
             "device",
             "device_id",
             "state",
             "device_name",
             "device_type",
             "created_at"


         ]
class roomsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Rooms
        fields = "__all__"

class buildingsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Buildings
        fields = "__all__"
class roomsSerializerHierarchy(serializers.ModelSerializer):
    devices = devicesSerializer(many=True)
    class Meta:
        model = Rooms
        fields = "__all__"

class buildingsSerializerHierarchy(serializers.ModelSerializer):
    rooms = roomsSerializerHierarchy(many=True)
    class Meta:
        model = Buildings
        fields = "__all__"

