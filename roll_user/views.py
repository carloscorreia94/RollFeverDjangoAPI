from django.shortcuts import render
from rest_framework.views import APIView
from oauth2_provider.ext.rest_framework import TokenHasReadWriteScope, TokenHasScope
from rest_framework import permissions
from spots.serializers import SpotSerializer
from spots.models import Spot
from rollfeverapi.common import validation_utils, validation_geo
from rollfeverapi.common import validation_messages
from rest_framework.response import Response
from .models import Favorites
from rest_framework import status
from rest_auth.models import MyUser

# Create your views here.
class UserFavorites(APIView):
    permission_classes = [permissions.IsAuthenticated, TokenHasScope]
    required_scopes = ['spot_guy']

    def get(self, request,user):

        favorites = Favorites.objects.filter(user=user).values_list('spot_id')
        spots = Spot.objects.filter(id__in = favorites)
        serializer = SpotSerializer(spots, many=True)
        return Response(validation_utils.output_success(validation_messages.type_field_set,serializer.data))


    def post(self, request,user,spot):
        #DO THIS PROPERLY
        #TODO : USING SERIALIZERS, VALIDATORS ETC
        favorite = Favorites()
        favorite.user = MyUser.objects.get(id=user)
        favorite.spot = Spot.objects.get(id=spot)
        favorite.save()

        return Response(validation_utils.output_success(validation_messages.type_content_created), status=status.HTTP_201_CREATED)

        #return Response(validation_utils.output_error(validation_messages.invalid_input_params,serializer.errors), status=status.HTTP_400_BAD_REQUEST)