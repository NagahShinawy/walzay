from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView


class HealthCheckAPIView(APIView):
    def get(self, request, *args, **kwargs):
        return Response(
            {"status": "Server is running smoothly!"}, status=status.HTTP_200_OK
        )
