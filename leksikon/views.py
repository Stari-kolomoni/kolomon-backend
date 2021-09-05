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
    serializer_class = serializers.QuickSearchSerializer

    @extend_schema(
        parameters=[OpenApiParameter(
            name='query',
            description='Search term',
            required=True, type=str)
        ]
    )
    @action(methods=['get'],
            detail=False,
            serializer_class=serializer_class)
    def quick(self, request: Request):
        """
        Perform a quick word search. Returns a list of quick search results ordered by decreasing relevance.
        """
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

        query = SearchQuery(request.query_params.get('query'))

        english_results = models.EnglishEntry.objects.annotate(
            rank=SearchRank(english_search_vector, query, cover_density=True)
        ).filter(rank__gt=0).order_by('-rank')
        slovene_results = models.Translation.objects.annotate(
            rank=SearchRank(slovene_search_vector, query, cover_density=True)
        ).filter(rank__gt=0).order_by('-rank')

        mixed_entries = []
        for english_entry in english_results:
            object = objects.Word(english_entry)
            mixed_entries.append(object)
        for slovene_entry in slovene_results:
            object = objects.Word(slovene_entry)
            mixed_entries.append(object)

        serializer = serializers.QuickSearchSerializer(mixed_entries, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
