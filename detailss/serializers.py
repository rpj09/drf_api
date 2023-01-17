from rest_framework import serializers
from .models import Drinks
from django.contrib.auth import authenticate

class DrinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Drinks
        fields = ['id','name','description']


