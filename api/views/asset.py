from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework import mixins
from rest_framework import generics
from rest_framework.decorators import detail_route, list_route
from rest_framework.response import Response
from rest_framework import status
from repository.models import *
from ..serializers.asset import *
from importlib import import_module


# class AssetViewSet(viewsets.ModelViewSet):
#     queryset = Asset.objects.all()
#     serializer_class = AssetSerializer
#     lookup_field = 'manufactory'

class AssetListView(APIView):
    def get_object_id(self, data, model_name, object_name):
        mod = import_module('repository.models')
        model_obj = getattr(mod, model_name)
        if isinstance(data.get(object_name, None), dict):
            obj_dict = data.pop(object_name)
            obj, _ = model_obj.objects.get_or_create(name=obj_dict['name'])
            data.update({object_name: obj.id})

    def get(self, request, format=None):
        assets = Asset.objects.all()
        serializer = AssetSerializer(assets, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        data = request.data
        self.get_object_id(data, 'Manufactory', 'manufactory')
        self.get_object_id(data, 'IDC', 'idc')
        self.get_object_id(data, 'BusinessUnit', 'business_unit')
        serializer = AssetSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class AssetDetailView(APIView):
    def get_object(self, pk):
        try:
            return Asset.objects.get(pk=pk)
        except Asset.DoesNotExist:
            return Http404

    def get(self, request, pk, format=None):
        asset = self.get_object(pk)
        serializer = AssetSerializer(asset)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        asset = self.get_object(pk)
        serializer = AssetSerializer(asset, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, format=None):
        asset = self.get_object(pk)
        serializer = AssetSerializer(asset, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    def delete(self, request, pk, format=None):
        asset = self.get_object(pk)
        asset.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ServerViewSet(viewsets.ModelViewSet):
    queryset = Server.objects.all()
    serializer_class = ServerSerializer


class DiskViewSet(viewsets.ModelViewSet):
    queryset = Disk.objects.all()
    serializer_class = DiskSerializer



class RaidAdaptorViewSet(viewsets.ModelViewSet):
    queryset = RaidAdaptor.objects.all()
    serializer_class = RaidAdaptorSerializer


class NetworkDeviceSet(viewsets.ModelViewSet):
    queryset = NetworkDevice.objects.all()
    serializer_class = NetworkDeviceSerializer


class NICViewSet(viewsets.ModelViewSet):
    queryset = Disk.objects.all()
    serializer_class = NICSerializer


class MemoryViewSet(viewsets.ModelViewSet):
    queryset = Memory.objects.all()
    serializer_class = MemorySerializer


class IDCViewSet(viewsets.ModelViewSet):
    queryset = IDC.objects.all()
    serializer_class = MemorySerializer


class BusinessUnitViewSet(viewsets.ModelViewSet):
    queryset = BusinessUnit.objects.all()
    serializer_class = MemorySerializer


class OperatorViewSet(viewsets.ModelViewSet):
    queryset = Operator.objects.all()
    serializer_class = MemorySerializer


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class ManufactoryViewSet(viewsets.ModelViewSet):
    queryset = Manufactory.objects.all()
    serializer_class = ManufactorySerializer
    lookup_field = 'manufactory'
    lookup_url_kwarg = 'manufactory'


# class ManufactoryDetailView(mixins.CreateModelMixin,
#                             mixins.RetrieveModelMixin,
#                             mixins.DestroyModelMixin,
#                             generics.GenericAPIView)
#
#     queryset = Manufactory.objects.all()
#     serializer_class = ManufactorySerializer
#
#     lookup_field = manufactory
#
#     def get(self, request, *args, **kwargs):
#         return self.get(request, *args, **kwargs)
#
#     def put(self,  request, *args, **kwargs):
#         return self.put(request, *args, **kwargs)
#
#     def delete(self, request, *args, **kwargs):
#         return self.delete(request, *args, **kwargs)




class AssetRecordViewSet(viewsets.ModelViewSet):
    queryset = Manufactory.objects.all()
    serializer_class = TagSerializer


class ErrorLogViewSet(viewsets.ModelViewSet):
    queryset = Manufactory.objects.all()
    serializer_class = TagSerializer