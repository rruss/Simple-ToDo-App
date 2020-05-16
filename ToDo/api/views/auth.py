from django.contrib.auth import authenticate
from django.shortcuts import render
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.generics import get_object_or_404, ListAPIView
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.views import APIView

from ..serializers import UserSerializer, LoginSerializer
from rest_framework.response import Response
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from ..models import MyUser
from rest_framework import status


class UserList(ListAPIView):
    queryset = MyUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated,)


@api_view(['POST'])
@renderer_classes([TemplateHTMLRenderer])
def login(request):
    serializer = AuthTokenSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = serializer.validated_data.get('user')
    user_obj = MyUser.objects.get(email=user)
    user_obj.is_logged = True
    token, created = Token.objects.get_or_create(user=user)
    token_str = f"Token ${token}"
    user_obj.token = token_str
    user_obj.save()
    context = {"token": token}

    return Response(context, headers={'Authorization': token_str}, template_name='main.html')


@api_view(['POST'])
def logout(request):
    user = request.user.email
    user_obj = MyUser.objects.get(email=user)
    user_obj.is_logged = False
    user_obj.save()
    request.auth.delete()
    return Response(status=status.HTTP_200_OK)
