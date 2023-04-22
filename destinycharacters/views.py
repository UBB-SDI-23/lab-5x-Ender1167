from dataclasses import dataclass

from django.db.models import Avg

from .models import Player, Weapon, Location, Location_Weapon
from .serializers import PlayerSerializer, WeaponSerializer, LocationSerializer, PlayerSerializer_No_Wep, WeaponSerializer_Detail
from .serializers import Location_WeaponSerializer, PlayerMaxReport, PlayerSerializer_No_Eq
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.generics import ListAPIView
from rest_framework import status
from django.views.generic import ListView

class Player_Weapons(ListAPIView):
    queryset = Weapon.objects.all()
    serializer_class = WeaponSerializer_Detail

    def get_queryset(self):
        return super().get_queryset().filter(
            id=self.kwargs['pk']
        )


@api_view(['GET', 'POST'])
def player_list(request):
    #read all
    if request.method == 'GET':
        players = Player.objects.all()[:10:-1]
        serializer = PlayerSerializer(players, many=True)
        return Response(serializer.data)

    #create 1
    if request.method == 'POST':
        serializer = PlayerSerializer_No_Eq(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            print(serializer.errors)

@api_view(['GET', 'POST'])
def player_list_no_weapons(request):
    #read all without weapons
    if request.method == 'GET':
        players = Player.objects.all()
        serializer = PlayerSerializer_No_Wep(players, many=True)
        return Response(serializer.data)

    if request.method == 'POST':
        serializer = PlayerSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

@api_view(['GET', 'POST'])
def location_list(request):
    #read all
    if request.method == 'GET':
        locations = Location.objects.all()
        serializer = LocationSerializer(locations, many=True)
        return Response(serializer.data)

    #create 1
    if request.method == 'POST':
        serializer = LocationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

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


@api_view(['GET', 'POST'])
def location_weapon_list(request):
    #read all
    if request.method == 'GET':
        wep_loc = Location_Weapon.objects.all()
        serializer = Location_WeaponSerializer(wep_loc, many=True)
        return Response(serializer.data)

    #create 1
    if request.method == 'POST':
        serializer = Location_WeaponSerializer(data=request.data)
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
def player_detail(request, pk):

    try:
        player = Player.objects.get(id=pk)
    except Player.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    #read 1
    if request.method == 'GET':
        serializer = PlayerSerializer(player)
        return Response(serializer.data)

    #update
    if request.method == 'PUT':
        serializer = PlayerSerializer(player, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        #delete
    if request.method == 'DELETE':
        player.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['POST'])
def player_add_weapons(request, pk):

    try:
        player = Player.objects.get(id=pk)
    except Player.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'POST':
        serializer = PlayerSerializer(player, data=request.data)

        if serializer.is_valid():
            new_weapons = serializer.save()
            player.weapons.add(*new_weapons)
            return Response(serializer.data)


@api_view(['GET', 'PUT', 'DELETE'])
def location_weapon_detail(request, pk):

    try:
        location_weapon = Location_Weapon.objects.get(id=pk)
    except Location_Weapon.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    #read 1
    if request.method == 'GET':
        serializer = Location_WeaponSerializer(location_weapon)
        return Response(serializer.data)

    #update
    if request.method == 'PUT':
        serializer = Location_WeaponSerializer(location_weapon, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    #delete
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

