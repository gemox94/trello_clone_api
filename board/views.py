from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import BasePermission, AllowAny, IsAuthenticated
from rest_framework.decorators import action

from . import serializers
from accounts import models as account_models


class AnonCreateAndUpdateOwnerOnly(BasePermission):
    """
    Custom permission:
        - allow anonymous POST
        - allow authenticated GET and PUT on *own* record
        - allow all actions for staff
    """

    def has_permission(self, request, view):
        return view.action == 'create' or request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        return view.action in ['retrieve', 'update', 'partial_update'] and obj.user.id == request.user.id or request.user.is_staff


class ManagerViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.ManagerSerializer

    def get_permissions(self):

        if self.action == 'create' or self.action == 'authenticate':
            permission_classes = [AllowAny]

        else:
            permission_classes = [IsAuthenticated]

        return [permission() for permission in permission_classes]

    def get_queryset(self):
        return account_models.User.objects.filter(rol_id=1)

    def create(self, request, *args, **kwargs):
        if 'password' in request.data:
            request.data['password'] = make_password(request.data['password'])
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        serializer.save(rol_id=1)

    @action(methods=['POST'], detail=False)
    def authenticate(self, request):
        data = request.data
        print(data)
        if 'email' not in data or 'password' not in data:
            return Response({'error': 'Invalid data'}, status=status.HTTP_400_BAD_REQUEST)

        user = authenticate(request, username=data['email'], password=data['password'])

        if user is not None:
            token, created = Token.objects.get_or_create(user=user)
            print(token.key)
            return Response({'token': token.key}, status=status.HTTP_200_OK)

        else:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)


class ProjectViewSet(viewsets.ModelViewSet):

    serializer_class = serializers.ProjectSerializer

    def perform_create(self, serializer):
        serializer.save(manager=self.request.user)

