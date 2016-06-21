from django.shortcuts import render
from rollfeverapi.common.views import GenericView
from rollfeverapi.common.output_messages import OutResponse


# Create your views here.
class UploadMedia(GenericView):

    def post(self, request, media_type, content_id):
        #TODO : Take into account that user can only upload stuff for its own content
        _status = {"upload" : "media", "media_type" : media_type, "content_id" : content_id}
        return OutResponse.action_performed(_status)
