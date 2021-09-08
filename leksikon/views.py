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
    return Response(serializer.data, status=status.HTTP_200_OK)


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

        word_list = []
        for result in results:
            word_obj = objects.Word(result)
            word_list.append(word_obj)

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

        word_list = []
        id_list = []
        for result in results:
            print(result.entry + " " + str(result.rank))
            query_obj = objects.Pair(result)
            if not query_obj.check_duplicates(id_list):
                word_list.append(query_obj)
                if query_obj.slovene:
                    id_list.append(query_obj.slovene.id)
                if query_obj.english:
                    id_list.append(query_obj.english.id)

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
