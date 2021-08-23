from django.contrib.auth.models import User
from rest_framework import serializers
from . import models


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'password')


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Category
        fields = '__all__'

    def is_duplicate(self):
        queryset = models.Category.objects.all()
        for query in queryset:
            if self.validated_data.get('name') == query.name:
                return True
        return False


class EnglishEntrySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.EnglishEntry
        fields = '__all__'
