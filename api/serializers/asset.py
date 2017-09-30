
from rest_framework import serializers
from drf_writable_nested import WritableNestedModelSerializer
from repository.models import *



class ManufactorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Manufactory
        fields = '__all__'


class AssetSerializer(serializers.ModelSerializer):
    # manufactory = ManufactorySerializer()
    class Meta:
        model = Asset
        fields = '__all__'


class ServerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Server
        fields = '__all__'


class NetworkDeviceSerializer(serializers.ModelSerializer):
    class Meta:
        model = NetworkDevice
        fields = '__all__'


class DiskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Disk
        fields = '__all__'


class RaidAdaptorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Disk
        fields = '__all__'


class NICSerializer(serializers.ModelSerializer):
    class Meta:
        model = Disk
        fields = '__all__'


class MemorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Disk
        fields = '__all__'


class IDCSerializer(serializers.ModelSerializer):
    class Meta:
        model = IDC
        fields = '__all__'


class BusinessUnitSerializer(serializers.ModelSerializer):
    class Meta:
        model = BusinessUnit
        fields = '__all__'


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('id', 'name',)


class OperatorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Operator
        fields = '__all__'




class AssetRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = Manufactory
        fields = '__all__'


class ErrorLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = Manufactory
        fields = '__all__'