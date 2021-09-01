from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank
from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework import status
from rest_framework.decorators import api_view, action
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
        """Lists all categories"""
        queryset = models.Category.objects.all().order_by('name')
        serializer = serializers.CategorySerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request: Request, *args, **kwargs):
        """Inserts a new category in the database"""
        serializer = serializers.CategorySerializer(data=request.data)
        if serializer.is_valid():
            if serializer.is_duplicate():
                return Response(serializer.errors, status=status.HTTP_409_CONFLICT)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request: Request, *args, **kwargs):
        """Updates the specific category with provided information"""
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
        """Returns the specific category"""
        object_id = self.kwargs.get('pk')
        try:
            query = models.Category.objects.get(id=object_id)
            serializer = serializers.CategorySerializer(query)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except models.Category.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def destroy(self, request: Request, *args, **kwargs):
        """Deletes the specific category from the database"""
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
        """Lists all English entries"""
        queryset = models.EnglishEntry.objects.all().order_by('entry')
        serializer = serializers.EnglishEntrySerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request: Request, *args, **kwargs):
        """Inserts a new English entry in the database"""
        serializer = serializers.EnglishEntrySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request: Request, *args, **kwargs):
        """Updates the specific English entry with provided information"""
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
        """Returns the specific English entry"""
        object_id = self.kwargs.get('pk')
        try:
            query = models.EnglishEntry.objects.get(id=object_id)
            serializer = serializers.EnglishEntrySerializer(query)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except models.EnglishEntry.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def destroy(self, request: Request, *args, **kwargs):
        """Deletes the specific English entry from the database"""
        object_id = self.kwargs.get('pk')
        try:
            query = models.EnglishEntry.objects.get(id=object_id)
            query.delete()
            return Response(status=status.HTTP_200_OK)
        except models.EnglishEntry.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name='search_term',
                description='A search term',
                required=True, type=str
            )
        ]
    )
    @action(detail=False, methods=['get'],
            serializer_class=serializers.EnglishEntrySerializer)
    def search(self, request: Request, *args, **kwargs):
        if 'search_term' in request.query_params:
            # TODO: Add weights to the search
            search_vector = SearchVector('entry',
                                         'translation_comment',
                                         'categories__name',
                                         'categories__description',
                                         'links__title',
                                         'links__link')
            query = SearchQuery(request.query_params.get('search_term'))
            results = models.EnglishEntry.objects.annotate(
                rank=SearchRank(search_vector, query, cover_density=True)
            ).filter(rank__gt=0).order_by('-rank')
            serializer = serializers.EnglishEntrySerializer(results, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['get', 'post'],
            serializer_class=serializers.SuggestionSerializer)
    def suggestions(self, request: Request, pk=None):
        """Operates on suggestions of the given English entry"""
        if pk:
            try:
                query = models.EnglishEntry.objects.get(id=pk)
                if request.method == 'GET':
                    serializer = serializers.EnglishEntrySerializer(query)
                    suggestion_list = serializer.data.get('suggestion_list')
                    return Response(suggestion_list, status=status.HTTP_200_OK)

                elif request.method == 'POST':
                    serializer = serializers.SuggestionSerializer(data=request.data)
                    if serializer.is_valid():
                        suggestion = serializer.save()
                        query.suggestions.add(suggestion)
                        return Response(serializer.data, status=status.HTTP_201_CREATED)

            except models.EnglishEntry.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)
        return Response(status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['put', 'delete'],
            serializer_class=serializers.SuggestionSerializer,
            url_path='suggestions/(?P<suggestion_id>[^/.]+)'
            )
    def suggestion(self, request: Request, pk=None, suggestion_id=None):
        """Operates on suggestions of the given English entry"""
        if pk:
            try:
                # This is here only to check if the English entry exists and prevent bad use
                query = models.EnglishEntry.objects.get(id=pk)
                try:
                    object_id = int(suggestion_id)
                    suggestion = models.Suggestion.objects.get(id=object_id)
                    if request.method == 'PUT':
                        serializer = serializers.SuggestionSerializer(data=request.data)
                        if serializer.is_valid():
                            serializer.update(suggestion, request.data)
                            return Response(status=status.HTTP_200_OK)
                    elif request.method == 'DELETE':
                        suggestion.delete()
                        return Response(status=status.HTTP_200_OK)
                except models.Suggestion.DoesNotExist:
                    return Response(status=status.HTTP_404_NOT_FOUND)
            except models.EnglishEntry.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)
        return Response(status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name='count',
                description='Number of returned entries',
                required=False, type=int
            ),
            OpenApiParameter(
                name='order_by',
                description='Which entries to return based on modification date. Accepts *any*, *edits*, *created*.'
                            ' Defaults to *any*.',
                required=False, type=str
            )
        ]
    )
    @action(detail=False, methods=['get'],
            serializer_class=serializers.EnglishEntrySerializer)
    def recent(self, request: Request, *args, **kwargs):
        """Lists all recent English entries based on their time of creation and/or modification"""
        count = 10
        if 'count' in request.query_params:
            count_request = request.query_params.get('count')
            if isinstance(count, int):
                count = int(count_request)

        order_type = ['-last_modified', '-created']
        if 'order_by' in request.query_params:
            order_by = request.query_params.get('order_by')
            if order_by == 'edits':
                order_type = ['-last_modified']
            elif order_by == 'created':
                order_type = ['-created']

        query = models.EnglishEntry.objects.order_by(*order_type)[:count]
        serializer = serializers.EnglishEntrySerializer(query, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class Translation(ModelViewSet):
    queryset = models.Translation.objects.all()
    serializer_class = serializers.TranslationSerializer
    http_method_names = ['get', 'post', 'delete', 'put']

    def list(self, request: Request, *args, **kwargs):
        """Lists all Slovene entries"""
        queryset = models.Translation.objects.all().order_by('translation')
        serializer = serializers.TranslationSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request: Request, *args, **kwargs):
        """Inserts a new Slovene entry in the database"""
        serializer = serializers.TranslationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request: Request, *args, **kwargs):
        """Updates the specified Slovene entry with provided information"""
        try:
            object_id = self.kwargs.get('pk')
            query = models.Translation.objects.get(id=object_id)
            serializer = serializers.TranslationSerializer(data=request.data)
            if serializer.is_valid():
                serializer.update(query, request.data)
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except models.Translation.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def retrieve(self, request: Request, *args, **kwargs):
        """Returns the specified Slovene entry"""
        object_id = self.kwargs.get('pk')
        try:
            query = models.Translation.objects.get(id=object_id)
            serializer = serializers.TranslationSerializer(query)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except models.Translation.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def destroy(self, request: Request, *args, **kwargs):
        """Deletes the specified Slovene entry from the database"""
        object_id = self.kwargs.get('pk')
        try:
            query = models.Translation.objects.get(id=object_id)
            query.delete()
            return Response(status=status.HTTP_200_OK)
        except models.Translation.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
