from rest_framework.views import APIView
from .models import Session
from spots.models import Spot
from .serializers import SessionSerializer
from rest_framework.response import Response
from rest_framework import status
from oauth2_provider.ext.rest_framework import TokenHasReadWriteScope, TokenHasScope
from rest_framework import permissions
from rollfeverapi.common import validation_utils, validation_geo
from rollfeverapi.common import validation_messages
from spots.logic import geo_utils
from rollfeverapi.common.views import GenericView
import base64
import binascii
from rollfeverapi.common.output_messages import OutResponse
from rollfeverapi.common.search_utils import session_search


# Create your views here.
class SessionList(APIView):
    # TODO : Do complete responses
    # No Permissions for now, just testing
    def get(self, request, spot):
        if Spot.objects.filter(id = spot).exists():
            # TODO: Take care of empty response
            spotSessions = Session.objects.filter(spot__id = spot)
            serializer = SessionSerializer(spotSessions,many=True)
            return Response(validation_utils.output_success(validation_messages.type_field_set,serializer.data))
        return Response(validation_utils.output_error(validation_messages.invalid_input_params), status=status.HTTP_400_BAD_REQUEST)

    def post(self, request, spot):
        if Spot.objects.filter(id = spot).exists():
            serializer = SessionSerializer(data=request.data)
            if serializer.is_valid():
                # TODO : Do this with an exception
                serializer.save(created_by=self.request.user, spot=Spot.objects.get(id=spot))
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(validation_utils.output_error(validation_messages.invalid_input_params), status=status.HTTP_400_BAD_REQUEST)


class SessionSearch(GenericView):

    def get(self, request, base64string):
        if base64string is None:
            #TODO: Get queryParams - do something without search
            decoded = None
        else:
            try:
                decoded = base64.b64decode(base64string).decode('utf-8')
            except binascii.Error:
                return OutResponse.invalid_arguments()

        search_results = session_search(decoded)
        if len(search_results) == 0:
            return OutResponse.empty_set()

        return OutResponse.content_set(search_results)