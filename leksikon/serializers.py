from django.contrib.auth.models import User
from rest_framework import serializers
from . import models


class PingSerializer(serializers.Serializer):
    message = serializers.CharField(max_length=50)


class EntryBasicSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    word = serializers.CharField(max_length=100)
    description = serializers.CharField()

    def update(self, instance, validated_data, **kwargs):
        if 'word' in validated_data:
            instance.entry = validated_data.get('word')
        if 'description' in validated_data:
            instance.use_case = validated_data.get('description')
        instance.save()


class QuickSearchSerializer(EntryBasicSerializer):
    language = serializers.CharField(max_length=10)


class FullSearchSerializer(serializers.Serializer):
    english = EntryBasicSerializer(allow_null=True)
    slovene = EntryBasicSerializer(allow_null=True)


class OrphanSerializer(EntryBasicSerializer):
    language = serializers.CharField(max_length=10)


class SuggestionSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    suggestion = serializers.CharField(max_length=100)
    separate_gender_form = serializers.BooleanField()
    comment = serializers.CharField()
    created_at = serializers.DateTimeField(read_only=True)
    edited_at = serializers.DateTimeField(read_only=True)

    def save(self, **kwargs):
        translation = self.validated_data.get('suggestion')
        gender_form = self.validated_data.get('separate_gender_form')
        description = self.validated_data.get('comment')
        instance = models.Suggestion(
            translation=translation,
            separate_gender_form=gender_form,
            description=description
        )
        instance.save()
        if 'entry' in kwargs:
            entry = kwargs.get('entry')
            entry.suggestions.add(instance)


class CategorySerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(max_length=100)
    description = serializers.CharField()


class LinkSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    title = serializers.CharField(max_length=100)
    url = serializers.CharField(max_length=100)


class RelatedSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField(read_only=True, max_length=100)


class EnglishSerializer(EntryBasicSerializer):
    translation_state = serializers.IntegerField(read_only=True)
    created_at = serializers.DateTimeField(read_only=True)
    edited_at = serializers.DateTimeField(read_only=True)

    def save(self, **kwargs):
        entry = self.validated_data.get('word')
        use_case = self.validated_data.get('description')
        instance = models.EnglishEntry(
            entry=entry,
            use_case=use_case
        )
        instance.save()


class ExtendedEnglishSerializer(EnglishSerializer):
    translation_comment = serializers.CharField(allow_blank=True)
    edited_by = serializers.IntegerField()
    categories = CategorySerializer(many=True)
    links = LinkSerializer(many=True)
    suggestions = SuggestionSerializer(many=True)
    related_words = RelatedSerializer(many=True)


class SloveneSerializer(EntryBasicSerializer):
    created_at = serializers.DateTimeField(read_only=True)
    edited_at = serializers.DateTimeField(read_only=True)
    word_female_form = serializers.CharField(max_length=100)
    type = serializers.CharField(max_length=100)
    related_word = RelatedSerializer(many=True)