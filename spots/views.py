from rest_framework.views import APIView
from .models import Spot
from .serializers import SpotSerializer, SpotNearbySerializer, SpotDetailSerializer
from rest_framework.response import Response
from rest_framework import status
from oauth2_provider.ext.rest_framework import TokenHasReadWriteScope, TokenHasScope
from rest_framework import permissions
from spotmaniaapi.common import validation_utils, validation_geo
from spotmaniaapi.common import validation_messages
from spots.logic import geo_utils
from django.http import Http404
from spotmaniaapi.common.views import GenericView
import base64
import binascii
from spotmaniaapi.common.output_messages import OutResponse
from spotmaniaapi.common.search_utils import spot_search



# Create your views here.

class SpotList(APIView):
    permission_classes = [permissions.IsAuthenticated, TokenHasScope]
    required_scopes = ['spot_guy']

    def get(self, request):

        spots = Spot.objects.all()
        serializer = SpotSerializer(spots, many=True)
        return Response(validation_utils.output_success(validation_messages.type_field_set,serializer.data))

    def post(self, request):
        serializer = SpotSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(created_by=self.request.user)
            return OutResponse.content_created_pending_media(serializer.data)
        return OutResponse.invalid_input_params(serializer.errors)

class SpotDetail(APIView):
    permission_classes = [permissions.IsAuthenticated, TokenHasScope]
    required_scopes = ['spot_guy']

    def get_object(self, spot):
        try:
            return Spot.objects.get(id=spot)
        except Spot.DoesNotExist:
            raise Http404

    def get(self, request, spot):
        spot = self.get_object(spot)
        serializer = SpotDetailSerializer(spot)
        return Response(serializer.data)


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

        serializer = SpotNearbySerializer(geo_utils.nearby(user_lat,user_lng,user_radius),many=True)
        return Response(serializer.data)


class SpotSearch(GenericView):

    def get(self, request, base64string):
        if base64string is None:
            #TODO: Get queryParams - do something without search
            decoded = None
        else:
            try:
                decoded = base64.b64decode(base64string).decode('utf-8')
            except binascii.Error:
                return OutResponse.invalid_arguments()

        search_results = spot_search(decoded)
        if len(search_results) == 0:
            return OutResponse.empty_set()

        return OutResponse.content_set(search_results)