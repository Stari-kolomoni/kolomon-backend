from django.contrib.auth.models import User
from rest_framework import serializers
from . import models


class PingSerializer(serializers.Serializer):
    message = serializers.CharField(max_length=50)


class EntryBasicSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    word = serializers.CharField(max_length=100)
    description = serializers.CharField()


class QuickSearchSerializer(EntryBasicSerializer):
    language = serializers.CharField(max_length=10)


class FullSearchSerializer(serializers.Serializer):
    english = EntryBasicSerializer(allow_null=True)
    slovene = EntryBasicSerializer(allow_null=True)

