from django.forms.models import model_to_dict
from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.response import Response

from ManageData.Serializers import StoreSerializer
from ManageData.models import StoreModel


# Create your views here.
class StoreViewSet(viewsets.ViewSet):
    serializer = StoreSerializer
    queryset = StoreModel.objects.all()

    def post(self, request):
        serializer = StoreSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            data = StoreModel.objects.all()
            if request.data.get('message') == "Load All Stores":
                datalist = [model_to_dict(item) for item in data]
                return Response(data= datalist, status=status.HTTP_200_OK)
            elif request.uuid is not None:
                uuid = serializer.validated_data['UUID']
                return Response(data=data.get(UUID = uuid), status=status.HTTP_200_OK)
            else:
                return Response("No Store Found", status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)

    def list(self, request):
        return Response("/ root path endpoint")