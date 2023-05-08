from rest_framework import serializers
from rest_framework.pagination import PageNumberPagination
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView

from .models import Player
from .models import Weapon
from .models import Location
from .models import Location_Weapon
from .models import *
from drf_writable_nested import WritableNestedModelSerializer

class WeaponSerializer(serializers.ModelSerializer):
    class Meta:
        model = Weapon
        fields = ['id', 'weapon_name', 'weapon_slot', 'weapon_element', 'weapon_type', 'weapon_damage', 'player_weapon']


class Location_WeaponSerializer(serializers.ModelSerializer):

    class Meta:
        model = Location_Weapon
        fields = ['id', 'drop_rate', 'wep', 'loc']



class WeaponSerializerIds(serializers.ModelSerializer):

    class Meta:
        model = Weapon
        fields = ['id']


class PlayerSerializer(WritableNestedModelSerializer, serializers.ModelSerializer):
    weapons = WeaponSerializer(source='weapon_set', many=True)
    nr_weapons = serializers.IntegerField()
    class Meta:
        model = Player
        ordering = ['-id']
        fields = ['id', 'name', 'class1', 'level', 'glimmer', 'shards', 'weapons', 'nr_weapons']


class PlayerSerializer_No_Eq(serializers.ModelSerializer):

    class Meta:
        model = Player
        fields = ['id', 'name', 'class1', 'level', 'glimmer', 'shards']

class WeaponSerializer_Detail(serializers.ModelSerializer):

    class Meta:
        model = Weapon
        fields = ['id', 'weapon_name', 'weapon_slot', 'weapon_element', 'weapon_type', 'weapon_damage', 'player_weapon']


class PlayerSerializer_No_Wep(serializers.ModelSerializer):

    weapons = WeaponSerializerIds(source='weapon_set', many=True)
    class Meta:
        model = Player
        fields = ['id', 'name', 'class1', 'level', 'glimmer', 'shards', 'weapons']


class LocationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Location
        fields = ['id', 'location_name', 'enemy_type', 'min_level', 'nr_public_events', 'nr_lost_sectors', 'all_weapons']
        depth = 1


class PlayerMaxReport(serializers.ModelSerializer):
    avg_weapon_dmg = serializers.FloatField()

    class Meta:
        model = Player
        fields = ['avg_weapon_dmg', 'name']



class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

class ProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(many=False, read_only=True)
    class Meta:
        model = UserProfile
        fields = ('user', 'bio', 'location', 'age', 'gender', 'marital_status')


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['username'] = user.username
        return token


