from base64 import b64decode
from dataclasses import dataclass

from django.db.models import Avg, Count
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAuthenticatedOrReadOnly
from rest_framework.views import APIView

from .models import Player, Weapon, Location, Location_Weapon, UserProfile
from .serializers import PlayerSerializer, WeaponSerializer, LocationSerializer, PlayerSerializer_No_Wep, \
    WeaponSerializer_Detail, UserLoginSerializer, ProfileSerializer, UserSerializer, RegisterSerializer
from .serializers import Location_WeaponSerializer, PlayerMaxReport, PlayerSerializer_No_Eq
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.generics import ListAPIView
from rest_framework import status, generics, permissions
from .paginators import StandardResultsSetPagination
from django.views.generic import ListView

from django.contrib.auth import authenticate
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render
import jwt

from .serializers import MyTokenObtainPairSerializer, TokenSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken

class Player_Weapons(ListAPIView):
    queryset = Weapon.objects.all()
    serializer_class = WeaponSerializer_Detail

    def get_queryset(self):
        return super().get_queryset().filter(
            id=self.kwargs['pk']
        )

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticatedOrReadOnly])
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
@permission_classes([IsAuthenticatedOrReadOnly])
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
@permission_classes([IsAuthenticatedOrReadOnly])
def location_list(request):
    #read all
    if request.method == 'GET':
        locations = Location.objects.all()
        #serializer = LocationSerializer(locations, many=True)

        paginator = StandardResultsSetPagination()
        paginated_locations = paginator.paginate_queryset(locations, request)
        serializer = LocationSerializer(paginated_locations, many=True)

        return paginator.get_paginated_response(serializer.data)
        #return Response(serializer.data)

    #create 1
    if request.method == 'POST':
        serializer = LocationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticatedOrReadOnly])
def weapon_list(request):
    #read all
    if request.method == 'GET':
        weapons = Weapon.objects.all()

        paginator = StandardResultsSetPagination()
        paginated_weapons = paginator.paginate_queryset(weapons, request)
        serializer = WeaponSerializer(paginated_weapons, many=True)

        return paginator.get_paginated_response(serializer.data)

        #serializer = WeaponSerializer(weapons, many=True)
        #return Response(serializer.data)

    #create 1
    if request.method == 'POST':
        serializer = WeaponSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticatedOrReadOnly])
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
@permission_classes([IsAuthenticatedOrReadOnly])
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
@permission_classes([IsAuthenticatedOrReadOnly])
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
@permission_classes([IsAuthenticatedOrReadOnly])
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
@permission_classes([IsAuthenticatedOrReadOnly])
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
@permission_classes([IsAuthenticatedOrReadOnly])
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
        locations_filtered = Location.objects.all().filter(min_level__gt=val)
        #serializer = LocationSerializer(locations_filtered, many=True)

        paginator = StandardResultsSetPagination()
        paginated_filtered_location = paginator.paginate_queryset(locations_filtered, request)
        serializer = LocationSerializer(paginated_filtered_location, many=True)

        return paginator.get_paginated_response(serializer.data)

        #return Response(serializer.data)
    

@api_view(['GET'])
def report1(request):

    if request.method == 'GET':
        queryset = Player.objects.all().annotate(avg_weapon_dmg=Avg('weapon__weapon_damage')).order_by('-avg_weapon_dmg')
        #print(queryset.query.__format__(''))
        paginator = StandardResultsSetPagination()
        paginated_report = paginator.paginate_queryset(queryset, request)
        serializer = PlayerMaxReport(paginated_report, many=True)

        return paginator.get_paginated_response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_profile(request):
    user = request.user
    profile = user.profile
    serializer = ProfileSerializer(profile, many=False)
    return Response(serializer.data)

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    refresh['username'] = user.username
    refresh['password'] = user.password
    return refresh

    #return {
    #    'refresh': str(refresh),
    #    'access': str(refresh.access_token),
    #}

@api_view(['GET', 'POST'])
def user_list(request):
    #read all
    if request.method == 'GET':
        users = UserProfile.objects.all()

        paginator = StandardResultsSetPagination()
        paginated_users = paginator.paginate_queryset(users, request)
        serializer = ProfileSerializer(paginated_users, many=True)

        return paginator.get_paginated_response(serializer.data)

    #create 1
    if request.method == 'POST':
        serializer = ProfileSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            print(serializer.errors)


#Register API
class RegisterApi(generics.GenericAPIView):
    serializer_class = RegisterSerializer

    def post(self, request, *args,  **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        #refresh1 = RefreshToken.for_user(user)
        refresh1 = get_tokens_for_user(user)

        return Response({
            "user": UserSerializer(user, context=self.get_serializer_context()).data,
            "message": "User Created Successfully.  Now perform Login to get your token",
            'refresh': str(refresh1),
            'access': str(refresh1.access_token),
        })


class RegisterFromToken(APIView):
    #permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    serializer_class = TokenSerializer

    def post(self, request, format=None):

        token1 = self.serializer_class(data=request.data)
        token_user = token1.initial_data['token']
        decoded_data = jwt.decode(jwt=token_user,
                                  key='django-insecure-zbuqt#d23hg7s406q_b2eu((to6l082br8t#h6yis5*xx@($vd',
                                  algorithms=["HS256"])
        token_user_username = decoded_data['username']
        token_user_password = decoded_data['password']

        if token_user_username != None:
            user = authenticate(username=token_user_username, password=token_user_password)
            if user.is_active == False:
                user.profile.isActive = False
                user.save()
                return Response({
                    "message": "Activation for" + token_user_username + " with password " + token_user_password + " is successful",
                })
            else:
                return Response({
                    "message": "Activation for" + token_user_username + " with password " + token_user_password + " failed",
                })
        else:
            return Response({
                "message": "Request is not a token.",
            })

        '''
        data1 = {}
        data1["username"] = token_user_username
        data1["password"] = token_user_password
        serializer = RegisterSerializer(data=data1)

        '''