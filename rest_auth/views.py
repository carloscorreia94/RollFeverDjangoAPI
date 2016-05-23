from rest_framework import generics
from rest_framework.views import APIView
from .permissions import IsAuthenticatedOrCreate
from .serializers import SignUpSerializer
from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework import status
from .models import MyUser
from rollfeverapi.common.output_messages import OutResponse
from oauth2_provider.views.base import TokenView
from rest_framework.parsers import JSONParser
from django.utils.decorators import method_decorator
from django.views.decorators.debug import sensitive_post_parameters
from rest_framework.request import Request
from django.http.request import HttpRequest
from django.http.response import HttpResponse
from rollfeverapi.common import validation_utils
import json
from json import JSONDecodeError

class SignUp(APIView):
    queryset = MyUser.objects.all()
    serializer_class = SignUpSerializer
    permission_classes = (IsAuthenticatedOrCreate,)

    def post(self, request, format=None):
        serializer = SignUpSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return OutResponse.content_created()
        return OutResponse.invalid_input_params(serializer.errors)


class Login(TokenView):

    @method_decorator(sensitive_post_parameters('password'))
    def post(self, request, *args, **kwargs):
        try:
            json_str=((request.body).decode('utf-8'))
            json_obj=json.loads(json_str)
        except JSONDecodeError:
            error = OutResponse.invalid_input_params().data
            return HttpResponse(json.dumps(error), content_type='application/json')

        if not validation_utils.check_args(json_obj,('username', 'password')):
            error = OutResponse.missing_input_params().data
            return HttpResponse(json.dumps(error), content_type='application/json')

        request.POST = { "grant_type" : "password", "scope" : "spot_guy",
                         "username" : json_obj["username"], "password" : json_obj["password"] }
        response = super(Login, self).post(request,args,kwargs)
        content = response.content.decode('utf-8')
        content = json.loads(content)

        if response.status_code == 200:
            content.pop("scope", None)
            content.pop("expires_in", None)
            content.pop("token_type", None)
            content = OutResponse.action_performed(content).data

        if response.status_code == 401:
            content = 'Invalid Credentials'
            content = OutResponse.invalid_input_params(content).data

        content = json.dumps(content)
        response.content = content.encode('utf-8')
        return response

#TODO : UpdatePassword, ManageSessions etc... here