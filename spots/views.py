from rest_framework.views import APIView
from .models import Spot
from .serializers import SpotSerializer
from rest_framework.response import Response
from rest_framework import status
from oauth2_provider.ext.rest_framework import TokenHasReadWriteScope, TokenHasScope
from rest_framework import permissions

# Create your views here.

class SpotList(APIView):
    permission_classes = [permissions.IsAuthenticated, TokenHasScope]
    required_scopes = ['spot_guy']

    def get(self, request):

        spots = Spot.objects.all()
        serializer = SpotSerializer(spots, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = SpotSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(created_by=self.request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)