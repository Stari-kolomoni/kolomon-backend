from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank
from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework import status, viewsets
from rest_framework.decorators import api_view, action
from rest_framework.request import Request
from rest_framework.response import Response

from . import objects, serializers, models


@api_view(['GET'])
def ping(request: Request):
    ping_obj = objects.Pong()
    serializer = serializers.PingSerializer(ping_obj)
    return Response(serializer.data, status=status.HTTP_418_IM_A_TEAPOT)


class SearchViewSet(viewsets.ViewSet):
    serializer_class = serializers.EntryBasicSerializer

    @extend_schema(
        parameters=[OpenApiParameter(
            name='query', description='Search term',
            required=True, type=str)
        ]
    )
    @action(methods=['get'], detail=False,
            serializer_class=serializers.QuickSearchSerializer)
    def quick(self, request: Request):
        """
        Perform a quick word search. Returns a list of quick search results ordered by decreasing relevance.
        """
        search_query = ""
        if 'query' in request.query_params:
            search_query = request.query_params.get('query')

        search_vector = SearchVector('entry',
                                     'use_case')
        query = SearchQuery(search_query)

        results = models.Word.objects.annotate(
            rank=SearchRank(search_vector, query, cover_density=True)
        ).filter(rank__gt=0).order_by('-rank')

        word_list = objects.Word.object_list(results)
        serializer = serializers.QuickSearchSerializer(word_list, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @extend_schema(
        parameters=[OpenApiParameter(
            name='query', description='Search term',
            required=True, type=str)
        ]
    )
    @action(methods=['get'], detail=False,
            serializer_class=serializers.FullSearchSerializer)
    def full(self, request: Request):
        """
            Perform a full search, returning translated word pairs if possible.
        """
        search_query = ""
        if 'query' in request.query_params:
            search_query = request.query_params.get('query')

        search_vector = SearchVector('entry',
                                     'use_case')
        query = SearchQuery(search_query)

        results = models.Word.objects.annotate(
            rank=SearchRank(search_vector, query)
        ).filter(rank__gt=0).order_by('-rank')

        word_list = objects.Pair.object_list(results)

        serializer = serializers.FullSearchSerializer(word_list, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class OrphanViewSet(viewsets.ViewSet):
    serializer_class = serializers.OrphanSerializer

    @extend_schema(
        parameters=[OpenApiParameter(
            name='count', description='Max number of returned elements',
            required=False, type=int
        ), OpenApiParameter(
            name='order_by', description='The way entries should be ordered',
            required=False, type=str
        )]
    )
    def list(self, request: Request):
        """
        Request a list of English/Slovene words that are missing their counterparts.
        """
        count = 100
        order_by = ''
        if 'count' in request.query_params:
            count = int(request.query_params.get('count'))
        if 'order_by' in request.query_params:
            order_by = request.query_params.get('order_by')

        if order_by == 'alphabetical':
            orphans = models.Word.objects.filter(englishentry__translations__isnull=True,
                                                 sloveneentry__englishentry__isnull=True).order_by('entry')[:count]
        else:
            orphans = models.Word.objects.filter(englishentry__translations__isnull=True,
                                                 sloveneentry__englishentry__isnull=True)[:count]
        word_list = []
        for orphan in orphans:
            orphan_obj = objects.Word(orphan)
            word_list.append(orphan_obj)
        serializer = serializers.OrphanSerializer(word_list, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


class EnglishViewSet(viewsets.ViewSet):
    serializer_class = serializers.EnglishSerializer

    def list(self, request: Request, *args, **kwargs):
        """
        Request a list of all English words in the dictionary
        """
        queryset = models.EnglishEntry.objects.all()
        object_list = objects.EnglishWord.object_list(queryset)
        serializer = serializers.EnglishSerializer(object_list, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request: Request, *args, **kwargs):
        """
        Submit a new English word.
        """
        serializer = serializers.EnglishSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(status=status.HTTP_201_CREATED)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(responses=serializers.ExtendedEnglishSerializer)
    def retrieve(self, request: Request, *args, **kwargs):
        """
        Request information about a specific English word.
        """
        if 'pk' in kwargs:
            instance_id = kwargs.get('pk')
            try:
                instance = models.EnglishEntry.objects.get(pk=instance_id)
                english_obj = objects.ExtendedEnglishWord(instance)
                serializer = serializers.ExtendedEnglishSerializer(english_obj)
                return Response(serializer.data, status=status.HTTP_200_OK)
            except models.EnglishEntry.DoesNotExist:
                return Response({}, status=status.HTTP_404_NOT_FOUND)
        return Response(status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request: Request, *args, **kwargs):
        """
        Modify an English word or its description.
        """
        if 'pk' in kwargs:
            instance_id = kwargs.get('pk')
            try:
                instance = models.EnglishEntry.objects.get(pk=instance_id)
                serializer = serializers.EntryBasicSerializer(data=request.data, partial=True)
                if serializer.is_valid():
                    serializer.update(instance, serializer.validated_data, user=request.user)
                    return Response(status=status.HTTP_200_OK)
                return Response(status=status.HTTP_400_BAD_REQUEST)
            except models.EnglishEntry.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)
        return Response(status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request: Request, *args, **kwargs):
        """
        Delete a specific English word entry.
        """
        if 'pk' in kwargs:
            instance_id = kwargs.get('pk')
            try:
                instance = models.EnglishEntry.objects.get(pk=instance_id)
                instance.delete()
                return Response(status=status.HTTP_200_OK)
            except models.EnglishEntry.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)
        return Response(status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(request=serializers.SuggestionSerializer,
                   responses=serializers.SuggestionSerializer)
    @extend_schema(description="Request an english word's translation suggestions.", methods=["GET"])
    @extend_schema(description="Submit a new translation suggestion for the english word.", methods=["POST"])
    @action(methods=['get', 'post'], detail=True, url_path='suggestions')
    def suggestions(self, request: Request, *args, **kwargs):
        if request.method == 'GET':
            return SuggestionViewSet.list(request, *args, **kwargs)
        elif request.method == 'POST':
            return SuggestionViewSet.create(request, *args, **kwargs)

    @extend_schema(request=serializers.SuggestionSerializer,
                   responses=serializers.SuggestionSerializer)
    @extend_schema(description="Get information about a specific translation suggestion.", methods=["GET"])
    @extend_schema(description="Edit a suggestion.", methods=["PATCH"])
    @extend_schema(description="Delete a suggestion.", methods=["DELETE"])
    @action(methods=['get', 'patch', 'delete'], detail=True, url_path='suggestions/<int:suggestion_id>')
    def suggestion_detail(self, request: Request, *args, **kwargs):
        if request.method == 'GET':
            return SuggestionViewSet.retrieve(request, *args, **kwargs)
        elif request.method == 'PATCH':
            return SuggestionViewSet.retrieve(request, *args, **kwargs)
        elif request.method == 'DELETE':
            return SuggestionViewSet.destroy(request, *args, **kwargs)

    @extend_schema(request=serializers.RelatedSerializer,
                   responses=serializers.RelatedSerializer)
    @extend_schema(description="Request related words for a specific english word.", methods=["GET"])
    @extend_schema(description="Add a related word to an english entry.", methods=["POST"])
    @action(methods=['get', 'post'], detail=True, url_path='related')
    def related_words(self, request: Request, *args, **kwargs):
        if request.method == 'GET':
            return RelatedViewSet.list(request, *args, **kwargs)
        elif request.method == 'POST':
            return RelatedViewSet.create(request, *args, **kwargs)

    @extend_schema(request=serializers.RelatedSerializer)
    @extend_schema(description="Remove the related word.", methods=["DELETE"])
    @action(methods=['delete'], detail=True, url_path='related/<int:related_id>')
    def related_word_detail(self, request: Request, *args, **kwargs):
        if request.method == 'DELETE':
            return RelatedViewSet.destroy(request, *args, **kwargs)

    @extend_schema(request=serializers.LinkSerializer)
    @extend_schema(description="Request a list of links associated with this english word.", methods=["GET"])
    @extend_schema(description="Add a new link to associate with the specifiec english word.", methods=["POST"])
    @action(methods=['get', 'post'], detail=True, url_path='links')
    def links(self, request: Request, *args, **kwargs):
        if request.method == 'GET':
            return LinkViewSet.list(request, *args, **kwargs)
        elif request.method == 'POST':
            return LinkViewSet.create(request, *args, **kwargs)

    @extend_schema(request=serializers.SuggestionSerializer,
                   responses=serializers.SuggestionSerializer)
    @extend_schema(description="Get information about a specific translation suggestion.", methods=["GET"])
    @extend_schema(description="Edit a suggestion.", methods=["PATCH"])
    @extend_schema(description="Delete a suggestion.", methods=["DELETE"])
    @action(methods=['get', 'patch', 'delete'], detail=True, url_path='links/<int:suggestion_id>')
    def link_detail(self, request: Request, *args, **kwargs):
        if request.method == 'GET':
            return LinkViewSet.retrieve(request, *args, **kwargs)
        elif request.method == 'PATCH':
            return LinkViewSet.partial_update(request, *args, **kwargs)
        elif request.method == 'DELETE':
            return LinkViewSet.destroy(request, *args, **kwargs)

    @action(methods=['get'], detail=True)
    def translation(self, request: Request, *args, **kwargs):
        pass


class SuggestionViewSet:

    @staticmethod
    def list(request: Request, *args, **kwargs):
        """
        Request an English word's translation suggestions.
        """
        if 'pk' in kwargs:
            instance_id = kwargs.get('pk')
            try:
                instance = models.EnglishEntry.objects.get(pk=instance_id)
                suggestion_objects = objects.Suggestion.object_list(instance.suggestions.all())
                serializer = serializers.SuggestionSerializer(suggestion_objects, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)
            except models.EnglishEntry.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)
        return Response(status=status.HTTP_400_BAD_REQUEST)

    @staticmethod
    def create(request: Request, *args, **kwargs):
        """
        Submit a new translation suggestion for the english word.
        """
        if 'pk' in kwargs:
            instance_id = kwargs.get('pk')
            try:
                instance = models.EnglishEntry.objects.get(pk=instance_id)
                serializer = serializers.SuggestionSerializer(data=request.data)
                if serializer.is_valid():
                    serializer.save(entry=instance)
                    return Response(status=status.HTTP_201_CREATED)
            except models.EnglishEntry.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)
        return Response(status=status.HTTP_400_BAD_REQUEST)

    @staticmethod
    def retrieve(request: Request,  *args, **kwargs):
        """
        Get information about a specific translation suggestion.
        """
        pass

    @staticmethod
    def partial_update(request: Request,  *args, **kwargs):
        """
        Edit a suggestion.
        """
        pass

    @staticmethod
    def destroy(request: Request, *args, **kwargs):
        """
        Delete a suggestion.
        """
        pass


class RelatedViewSet:

    @staticmethod
    def list(request: Request, *args, **kwargs):
        pass

    @staticmethod
    def create(request: Request, *args, **kwargs):
        pass

    @staticmethod
    def destroy(request: Request, *args, **kwargs):
        pass


class LinkViewSet:

    @staticmethod
    def list(request: Request, *args, **kwargs):
        pass

    @staticmethod
    def create(request: Request, *args, **kwargs):
        pass

    @staticmethod
    def retrieve(request: Request, *args, **kwargs):
        pass

    @staticmethod
    def partial_update(request: Request, *args, **kwargs):
        pass

    @staticmethod
    def destroy(request: Request, *args, **kwargs):
        pass


class TranslationViewSet:

    @staticmethod
    def list(request: Request, *args, **kwargs):
        pass
