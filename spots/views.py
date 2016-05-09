from rest_framework.views import APIView
from .models import Spot
from .serializers import SpotSerializer
from rest_framework.response import Response
from rest_framework import status
from oauth2_provider.ext.rest_framework import TokenHasReadWriteScope, TokenHasScope
from rest_framework import permissions
from rollfeverapi.common import validation_utils, validation_geo
from rollfeverapi.common import validation_messages

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

class SpotsNearby(APIView):
    permission_classes = [permissions.IsAuthenticated, TokenHasScope]
    required_scopes = ['spot_guy']

    def get(self, request):
        params = request.query_params
        user_lat = params.get('lat', None)
        user_lng = params.get('lng', None)
        user_radius = params.get('radius',None) if 'radius' in params.keys() else validation_geo.DEFAULT_RADIUS
        args = ('lat', 'lng')

        if not validation_utils.check_args(params,args):
            return Response(validation_utils.output_error(validation_messages.message_missing_input_params), status=status.HTTP_400_BAD_REQUEST)
        if 'radius' in params.keys() and not validation_geo.check_radius(params.get('radius')):
            return Response(validation_utils.output_error(validation_messages.invalid_input_params), status=status.HTTP_400_BAD_REQUEST)
        if not validation_geo.check_coordinates(user_lat,user_lng):
            return Response(validation_utils.output_error(validation_messages.invalid_input_params), status=status.HTTP_400_BAD_REQUEST)

        return Response(Spot.nearby(user_lat,user_lng,user_radius))