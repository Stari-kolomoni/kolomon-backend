from django.contrib.auth.models import User
from rest_framework import serializers
from . import models


class PingSerializer(serializers.Serializer):
    message = serializers.CharField(max_length=50)


class QuickSearchSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    language = serializers.CharField(max_length=10)
    word = serializers.CharField(max_length=100)
    description = serializers.CharField()

