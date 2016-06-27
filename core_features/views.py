from django.shortcuts import render
from rollfeverapi.common.views import GenericView
from rollfeverapi.common.output_messages import OutResponse
from spots.models import Spot
from spots.serializers import SpotMainPicSerializer
from rest_auth.serializers import ProfilePictureSerializer
from django.db.models import ObjectDoesNotExist
from .models import PendingMedia
from rest_auth.models import Profile


# Create your views here.
class UploadMedia(GenericView):

    def __init__(self):
        self.content_id = None
        self.request = None

    def post(self, request, media_type, content_id):
        self.content_id = content_id
        self.request = request
        type_cases = {
            Spot.MEDIA_TYPE: self.handle_spot(),
            Profile.MEDIA_TYPE: self.handle_profile_picture()
        }
        return type_cases.get(media_type, OutResponse.invalid_arguments("wrong_media_type"))

    def handle_spot(self):
        try:
            if self.content_id is None:
                return OutResponse.invalid_arguments()

            actual_spot = Spot.all_objects.get(id=self.content_id,created_by=self.request.user.id)
            serializer = SpotMainPicSerializer(actual_spot, data=self.request.data)
            if serializer.is_valid():
                serializer.save()
                PendingMedia.update_pending_media(Spot.MEDIA_TYPE, self.content_id, 1)
                return OutResponse.content_updated()
            return OutResponse.invalid_input_params(serializer.errors)
        except ObjectDoesNotExist:
            return OutResponse.content_not_matched()

    def handle_profile_picture(self):
        try:
            actual_profile = Profile.objects.get(account=self.request.user.id)
            serializer = ProfilePictureSerializer(actual_profile,data=self.request.data)
            if serializer.is_valid():
                serializer.save()
                return OutResponse.content_updated()
            return OutResponse.invalid_input_params(serializer.errors)

        except ObjectDoesNotExist:
            return OutResponse.content_not_matched()
