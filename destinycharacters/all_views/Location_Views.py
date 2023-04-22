
from django.db.models import Avg

from destinycharacters_project.destinycharacters.models import Player, Weapon, Location, Location_Weapon
from destinycharacters_project.destinycharacters.serializers import PlayerSerializer, WeaponSerializer, LocationSerializer, PlayerSerializer_No_Wep, WeaponSerializer_Detail
from destinycharacters_project.destinycharacters.serializers import Location_WeaponSerializer, PlayerMaxReport, PlayerSerializer_No_Eq
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.generics import ListAPIView
from rest_framework import status

@api_view(['GET', 'PUT', 'DELETE'])
def location_weapon_detail(request, pk):

    try:
        location_weapon = Location_Weapon.objects.get(id=pk)
    except Location_Weapon.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    # read 1
    if request.method == 'GET':
        serializer = Location_WeaponSerializer(location_weapon)
        return Response(serializer.data)

    # update
    if request.method == 'PUT':
        serializer = Location_WeaponSerializer(location_weapon, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # delete
    if request.method == 'DELETE':
        location_weapon.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)



@api_view(['GET'])
def location_filter(request, val):

    if request.method == 'GET':
        locations_filtered = Location.objects.all().filter(min_level__gt=val)[:10:-1]
        serializer = LocationSerializer(locations_filtered, many=True)
        return Response(serializer.data)


@api_view(['GET'])
def report1(request):

    if request.method == 'GET':
        queryset = Player.objects.all().annotate(avg_weapon_dmg=Avg('weapon__weapon_damage')).order_by('-avg_weapon_dmg')[:100:-1]
        serializer = PlayerMaxReport(queryset, many=True)
        return Response(serializer.data)


@api_view(['GET', 'PUT', 'DELETE'])
def location_detail(request, pk):

    try:
        location = Location.objects.get(id=pk)
    except Location.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    #read 1
    if request.method == 'GET':
        serializer = LocationSerializer(location)
        return Response(serializer.data)

    #update
    if request.method == 'PUT':
        serializer = LocationSerializer(location, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    #delete
    if request.method == 'DELETE':
        location.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['GET', 'PUT', 'DELETE'])
def location_detail(request, pk):

    try:
        location = Location.objects.get(id=pk)
    except Location.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    #read 1
    if request.method == 'GET':
        serializer = LocationSerializer(location)
        return Response(serializer.data)

    #update
    if request.method == 'PUT':
        serializer = LocationSerializer(location, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    #delete
    if request.method == 'DELETE':
        location.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

