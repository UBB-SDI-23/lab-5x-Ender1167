
from django.db.models import Avg

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
        players = Player.objects.all()
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