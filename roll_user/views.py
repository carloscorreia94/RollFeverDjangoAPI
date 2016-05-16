from django.shortcuts import render
from rest_framework.views import APIView
from oauth2_provider.ext.rest_framework import TokenHasReadWriteScope, TokenHasScope
from rest_framework import permissions
from spots.serializers import SpotSerializer
from spots.models import Spot
from .models import Favorites
from rollfeverapi.common import validation_utils, validation_geo, output_messages
from rollfeverapi.common import validation_messages
from rollfeverapi.common.output_messages import OutResponse
from rest_framework.response import Response
from .models import Favorites
from rest_framework import status
from rest_auth.models import MyUser
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.decorators import api_view


# Create your views here.
class UserFavorites(APIView):
    permission_classes = [permissions.IsAuthenticated, TokenHasScope]
    required_scopes = ['spot_guy']

    def get(self, request,spot = None, username = None):
        if spot is not None:
            return OutResponse.page_not_found()

        try:
            inUser = request.user if username is None else MyUser.objects.get(username=username)
        except ObjectDoesNotExist:
            return OutResponse.invalid_arguments()

        favorites = Favorites.objects.filter(user=inUser).values_list('spot_id')
        spots = Spot.objects.filter(id__in = favorites)
        serializer = SpotSerializer(spots, many=True)
        return Response(validation_utils.output_success(validation_messages.type_field_set,serializer.data))

    def delete(self, request,spot, username = None):
        if username is not None:
            return OutResponse.page_not_found()

        try:
            inUser = request.user
            inSpot = Spot.objects.get(id=spot)
        except ObjectDoesNotExist:
            return OutResponse.invalid_arguments()

        same_favorite = Favorites.objects.filter(user=inUser, spot=inSpot)

        if not same_favorite.exists():
            return OutResponse.entry_not_existent()

        same_favorite.delete()

        return OutResponse.content_deleted()

    def post(self, request,spot, username =None):
        if username is not None:
            return OutResponse.page_not_found()

        try:
            inUser = request.user
            inSpot = Spot.objects.get(id=spot)
        except ObjectDoesNotExist:
            return OutResponse.invalid_arguments()

        same_favorite = Favorites.objects.filter(user=inUser, spot=inSpot)
        if same_favorite.exists():
            return OutResponse.entry_already_exists()

        favorite = Favorites()
        favorite.user = inUser
        favorite.spot = inSpot
        favorite.save()

        return OutResponse.content_created({'favorite_id': favorite.id})