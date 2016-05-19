from rest_framework import generics
from rest_framework.views import APIView
from .permissions import IsAuthenticatedOrCreate
from .serializers import SignUpSerializer
from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework import status
from .models import MyUser


class SignUp(APIView):
    queryset = MyUser.objects.all()
    serializer_class = SignUpSerializer
    permission_classes = (IsAuthenticatedOrCreate,)

    def post(self, request, format=None):
        serializer = SignUpSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


#TODO : UpdatePassword, ManageSessions etc... here