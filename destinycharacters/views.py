from dataclasses import dataclass

from django.db.models import Count, Max

from .models import Player, Weapon, Location, Location_Weapon
from .serializers import PlayerSerializer, WeaponSerializer, LocationSerializer, PlayerSerializer_No_Wep, WeaponSerializer_Detail
from .serializers import Location_WeaponSerializer, PlayerMaxReport
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
        players = Player.objects.all()
        serializer = PlayerSerializer(players, many=True)
        return Response(serializer.data)

    #create 1
    if request.method == 'POST':
        serializer = PlayerSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

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
        weapon = Weapon.objects.get(id=pk)

    except Weapon.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    #read 1
    if request.method == 'GET':
        serializer = WeaponSerializer_Detail(weapon, many=True)
        return Response(serializer.data)

    #update
    if request.method == 'PUT':
        serializer = WeaponSerializer(weapon, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    #delete
    if request.method == 'DELETE':
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


@api_view(['GET'])
def location_filter(request, val):

    if request.method == 'GET':
        locations_filtered = Location.objects.all().filter(min_level__gt=val)
        serializer = LocationSerializer(locations_filtered, many=True)
        return Response(serializer.data)





@dataclass
class ReportEntry:
    max1: int
    player: Player

@api_view(['GET'])
def report1(request):

    if request.method == 'GET':
        queryset = Player.objects.all().annotate(num_weapons=Count('weapon')).order_by('-num_weapons')
        max_nr_weapons = queryset[0].num_weapons

        serializer = PlayerMaxReport(queryset, many=True, context={'max_nr_weapons': max_nr_weapons})
        return Response(serializer.data)

