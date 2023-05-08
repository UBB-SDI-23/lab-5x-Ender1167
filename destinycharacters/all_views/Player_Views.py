
from django.db.models import Avg, Count

from destinycharacters.paginators import StandardResultsSetPagination
from destinycharacters_project.destinycharacters.models import Player, Weapon, Location, Location_Weapon
from destinycharacters_project.destinycharacters.serializers import PlayerSerializer, WeaponSerializer, LocationSerializer, PlayerSerializer_No_Wep, WeaponSerializer_Detail
from destinycharacters_project.destinycharacters.serializers import Location_WeaponSerializer, PlayerMaxReport, PlayerSerializer_No_Eq
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
        players = Player.objects.all().annotate(nr_weapons=Count('weapon__player_weapon'))

        paginator = StandardResultsSetPagination()
        paginated_players = paginator.paginate_queryset(players, request)
        serializer = PlayerSerializer(paginated_players, many=True)

        return paginator.get_paginated_response(serializer.data)

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
