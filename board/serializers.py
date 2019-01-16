from rest_framework import serializers
from rest_framework.authtoken.models import Token as DRF_Token

from accounts import models as account_models
from . import models


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Project
        fields = (
            'id',
            'name',
        )


class BoardSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Board
        fields = (
            'id',
            'name',
        )


class CardSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Card
        fields = (
            'id',
            'name',
            'description',
        )


class ManagerSerializer(serializers.ModelSerializer):
    class Meta:
        model = account_models.User
        fields = (
            'id',
            'name',
            'last_name',
            'email',
            'password',
        )
        extra_kwargs = {
            'password': {'write_only': True}
        }


class TokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = DRF_Token
        fields = (
            'key',
        )
