from django.contrib.auth.models import User
from rest_framework import serializers
from . import models


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'password')


class GenderVariantSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.GenderVariant
        fields = '__all__'


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


class SuggestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Suggestion
        fields = '__all__'


class LinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Link
        fields = '__all__'


class TranslationSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Translation
        fields = '__all__'


class EnglishEntrySerializer(serializers.ModelSerializer):
    category_list = CategorySerializer(source='categories', many=True, read_only=True)
    link_list = LinkSerializer(source='links', many=True, read_only=True)
    suggestion_list = SuggestionSerializer(source='suggestions', many=True, read_only=True)
    translation_list = TranslationSerializer(source='translations', many=True, read_only=True)

    class Meta:
        model = models.EnglishEntry
        fields = '__all__'
