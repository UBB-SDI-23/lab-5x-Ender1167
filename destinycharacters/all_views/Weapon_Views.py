from django.db.models import Avg

from destinycharacters_project.destinycharacters.models import Player, Weapon, Location, Location_Weapon
from destinycharacters_project.destinycharacters.serializers import PlayerSerializer, WeaponSerializer, LocationSerializer, PlayerSerializer_No_Wep, WeaponSerializer_Detail
from destinycharacters_project.destinycharacters.serializers import Location_WeaponSerializer, PlayerMaxReport, PlayerSerializer_No_Eq
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.generics import ListAPIView
from rest_framework import status
from django.views.generic import ListView

@api_view(['GET', 'POST'])
def weapon_list(request):
    #read all
    if request.method == 'GET':
        weapons = Weapon.objects.all()
        serializer = WeaponSerializer(weapons, many=True)
        return Response(serializer.data)

    #create 1
    if request.method == 'POST':
        serializer = WeaponSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

@api_view(['GET', 'PUT', 'DELETE'])
def weapon_detail(request, pk):

    try:
        weapon = Weapon.objects.filter(id=pk)

    except Weapon.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    #read 1
    if request.method == 'GET':
        weapon = Weapon.objects.filter(id=pk)
        serializer = WeaponSerializer(weapon, many=True)
        return Response(serializer.data)

    #update
    if request.method == 'PUT':
        weapon = Weapon.objects.get(id=pk)
        serializer = WeaponSerializer(weapon, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    #delete
    if request.method == 'DELETE':
        weapon = Weapon.objects.get(id=pk)
        weapon.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)