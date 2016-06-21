from django.shortcuts import render
from rollfeverapi.common.views import GenericView
from rollfeverapi.common.output_messages import OutResponse
from spots.models import Spot
from spots.serializers import SpotMainPicSerializer
from django.db.models import ObjectDoesNotExist


# Create your views here.
class UploadMedia(GenericView):

    def __init__(self):
        self.content_id = None
        self.request = None

    def post(self, request, media_type, content_id):
        self.content_id = content_id
        self.request = request
        type_cases = {
            Spot.MEDIA_TYPE: self.handle_spot()
        }
        return type_cases.get(media_type, OutResponse.invalid_arguments("wrong_media_type"))

    def handle_spot(self):
        try:
            actual_spot = Spot.objects.get(id=self.content_id)
            serializer = SpotMainPicSerializer(actual_spot, data=self.request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return OutResponse.content_updated()
            return OutResponse.invalid_input_params(serializer.errors)
        except ObjectDoesNotExist:
            return OutResponse.content_not_matched()
