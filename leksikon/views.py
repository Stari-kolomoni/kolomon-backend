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
            name='query',
            description='Search term',
            required=True, type=str)
        ]
    )
    @action(methods=['get'],
            detail=False,
            serializer_class=serializers.QuickSearchSerializer)
    def quick(self, request: Request):
        """
        Perform a quick word search. Returns a list of quick search results ordered by decreasing relevance.
        """
        search_query = ""
        if 'query' in request.query_params:
            search_query = request.query_params.get('query')

        slovene_search_vector = SearchVector('translation',
                                             'description',
                                             'female_form')
        english_search_vector = SearchVector('entry',
                                             'use_case',
                                             'translation_comment',
                                             'categories__name',
                                             'categories__description',
                                             'links__title',
                                             'links__link')

        query = SearchQuery(search_query)

        english_results = models.EnglishEntry.objects.annotate(
            rank=SearchRank(english_search_vector, query, cover_density=True)
        ).filter(rank__gt=0).order_by('-rank')
        slovene_results = models.Translation.objects.annotate(
            rank=SearchRank(slovene_search_vector, query, cover_density=True)
        ).filter(rank__gt=0).order_by('-rank')

        mixed_entries = []
        for english_entry in english_results:
            english_obj = objects.Word(english_entry)
            mixed_entries.append(english_obj)
        for slovene_entry in slovene_results:
            slovene_obj = objects.Word(slovene_entry)
            mixed_entries.append(slovene_obj)

        serializer = serializers.QuickSearchSerializer(mixed_entries, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @extend_schema(
        parameters=[OpenApiParameter(
            name='query',
            description='Search term',
            required=True, type=str)
        ]
    )
    @action(methods=['get'],
            detail=False,
            serializer_class=serializers.FullSearchSerializer)
    def full(self, request: Request):
        """
            Perform a full search, returning translated word pairs if possible.
        """
        search_query = ""
        if 'query' in request.query_params:
            search_query = request.query_params.get('query')

        # TODO: Optimize this!
        slovene_search_vector = SearchVector('translation',
                                             'description',
                                             'female_form')
        english_search_vector = SearchVector('entry',
                                             'use_case',
                                             'translation_comment',
                                             'categories__name',
                                             'categories__description',
                                             'links__title',
                                             'links__link',
                                             'translations__translation',
                                             'translations__description',
                                             'translations__female_form')

        query = SearchQuery(search_query)

        english_results = models.EnglishEntry.objects.annotate(
            rank=SearchRank(english_search_vector, query, cover_density=True)
        ).filter(rank__gt=0).order_by('-rank')
        slovene_results = models.Translation.objects.annotate(
            rank=SearchRank(slovene_search_vector, query, cover_density=True)
        ).filter(rank__gt=0).order_by('-rank')

        mixed_entries = []
        for english_entry in english_results:
            english_obj = objects.Pair(english_entry)
            mixed_entries.append(english_obj)
        for slovene_entry in slovene_results:
            if not slovene_entry.englishentry_set.all():
                slovene_obj = objects.Pair(slovene_entry)
                mixed_entries.append(slovene_obj)
        print(mixed_entries)

        serializer = serializers.FullSearchSerializer(mixed_entries, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
