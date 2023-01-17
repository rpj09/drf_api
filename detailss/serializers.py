from rest_framework import serializers
from .models import Drinks
from django.contrib.auth import authenticate,get_user_model

User = get_user_model()

class DrinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Drinks
        fields = ['id','name','description']


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(required=True,write_only=True)
    password2 = serializers.CharField(required=True,write_only=True)
    class Meta:
        model = User
        fields = ['id','username','email','password','password2']
        extra_kwargs = {
            'password':{'write_only':True},
            'password2':{'write_only':True},
        }
    def create(self, validated_data):
        username = validated_data['username']
        email = validated_data['email']
        password = validated_data['password']
        password2 = validated_data['password2']

        if password == password2:
            user = User(username=username,email=email)
            user.set_password(password)
            user.save()
            return user
        else:
            raise serializers.ValidationError("Passwords don't match")
        #return super().create(validated_data)
