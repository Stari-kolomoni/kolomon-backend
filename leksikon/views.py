from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from . import models
from . import serializers


@api_view(['GET'])
def ping(request: Request):
    data = {
        "message": "Pong!"
    }
    return Response(data, status=status.HTTP_200_OK)


class Category(ModelViewSet):
    queryset = models.EnglishEntry.objects.all()
    serializer_class = serializers.CategorySerializer
    http_method_names = ['get', 'post', 'delete', 'put']

    def list(self, request: Request, *args, **kwargs):
        queryset = models.Category.objects.all().order_by('name')
        serializer = serializers.CategorySerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request: Request, *args, **kwargs):
        serializer = serializers.CategorySerializer(data=request.data)
        if serializer.is_valid():
            if serializer.is_duplicate():
                return Response(serializer.errors, status=status.HTTP_409_CONFLICT)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request: Request, *args, **kwargs):
        try:
            object_id = self.kwargs.get('pk')
            query = models.Category.objects.get(id=object_id)
            serializer = serializers.CategorySerializer(data=request.data)
            if serializer.is_valid():
                serializer.update(query, request.data)
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except models.Category.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def retrieve(self, request: Request, *args, **kwargs):
        object_id = self.kwargs.get('pk')
        try:
            query = models.Category.objects.get(id=object_id)
            serializer = serializers.CategorySerializer(query)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except models.Category.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def destroy(self, request: Request, *args, **kwargs):
        object_id = self.kwargs.get('pk')
        try:
            query = models.Category.objects.get(id=object_id)
            query.delete()
            return Response(status=status.HTTP_200_OK)
        except models.Category.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)


class EnglishEntry(ModelViewSet):
    queryset = models.EnglishEntry.objects.all()
    serializer_class = serializers.EnglishEntrySerializer
    http_method_names = ['get', 'post', 'delete', 'put']

    def list(self, request: Request, *args, **kwargs):
        queryset = models.EnglishEntry.objects.all().order_by('entry')
        serializer = serializers.EnglishEntrySerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request: Request, *args, **kwargs):
        serializer = serializers.EnglishEntrySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request: Request, *args, **kwargs):
        try:
            object_id = self.kwargs.get('pk')
            query = models.EnglishEntry.objects.get(id=object_id)
            serializer = serializers.EnglishEntrySerializer(data=request.data)
            if serializer.is_valid():
                serializer.update(query, request.data)
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except models.EnglishEntry.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def retrieve(self, request: Request, *args, **kwargs):
        object_id = self.kwargs.get('pk')
        try:
            query = models.EnglishEntry.objects.get(id=object_id)
            serializer = serializers.EnglishEntrySerializer(query)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except models.EnglishEntry.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def destroy(self, request: Request, *args, **kwargs):
        object_id = self.kwargs.get('pk')
        try:
            query = models.EnglishEntry.objects.get(id=object_id)
            query.delete()
            return Response(status=status.HTTP_200_OK)
        except models.EnglishEntry.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
