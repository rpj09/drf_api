from django.http import JsonResponse
from .models import Drinks
from .serializers import DrinkSerializer
from rest_framework.decorators import api_view,permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions
from rest_framework.permissions import IsAuthenticated
from rest_framework import views
from . import serializers
from rest_framework_simplejwt.tokens import RefreshToken
import rest_framework_simplejwt

@api_view(['GET','POST'])
@permission_classes([IsAuthenticated])
def drinklist(request,format=None):



    if request.method=='GET':
        drinks = Drinks.objects.all()
        serializer = DrinkSerializer(drinks,many=True)
        return Response(serializer.data)
    if request.method=='POST':
        serializer = DrinkSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)

@api_view(['GET','PUT',"DELETE"])
@permission_classes([IsAuthenticated])
def details(request,id,format=None):

    try:
        drinks = Drinks.objects.get(pk=id)
    except Drinks.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        serializer = DrinkSerializer(drinks)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = DrinkSerializer(drinks,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        drinks.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class RegisterAPIView(views.APIView):
    serializer_class = serializers.RegisterSerializer

    def post(self,request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.save()
        
            refresh = RefreshToken.for_user(user)

            response_data = {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'username': serializer.data['username'],
                'email': serializer.data['email'],
            }
            return Response(response_data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

