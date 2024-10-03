from rest_framework import serializers

from . models import *


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = '__all__'
        read_only_fields = ['user']
