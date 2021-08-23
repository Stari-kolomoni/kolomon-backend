from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView


class Test(APIView):

    def get(self, request: Request):
        data = {
            "message": "Pong!"
        }
        return Response(data, status=status.HTTP_200_OK)
