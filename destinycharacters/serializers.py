from django.contrib.auth import authenticate
from rest_framework import serializers
from rest_framework.pagination import PageNumberPagination
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView

from .models import Player
from .models import Weapon
from .models import Location
from .models import Location_Weapon
from .models import *
from drf_writable_nested import WritableNestedModelSerializer
import datetime
from datetime import date
from rest_framework.exceptions import AuthenticationFailed

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

''' 
class ProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(many=False, read_only=True)
    class Meta:
        model = UserProfile
        fields = ('user', 'bio', 'location', 'age', 'gender', 'marital_status')
'''
from django.contrib.auth.hashers import make_password
class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['username'] = user.username
        token['password'] = user.password
        return token



    def validate_password(self, value: str) -> str:
        """
        Hash value passed by user.

        :param value: password of a user
        :return: a hashed version of the password
        """
        return make_password(value)


class UserRegistrationSerializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length=50, min_length=4)
    password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ['username', 'password']

    def validate(self, args):
        username = args.get('username', None)
        if User.objects.filter(username=username).exists():
            raise serializers.ValidationError('Username already exists!')
        return super().validate(args)

    def validate_password(self,value):
        """
        Validate that a password meets certain complexity requirements:
        - at least 8 characters long
        - contains at least one uppercase letter
        - contains at least one lowercase letter
        - contains at least one digit
        - contains at least one special character
        """
        if len(value) < 8:
            raise serializers.ValidationError("The password must be at least 8 characters long.")
        if not any(char.isupper() for char in value):
            raise serializers.ValidationError("The password must contain at least one uppercase letter.")
        if not any(char.islower() for char in value):
            raise serializers.ValidationError("The password must contain at least one lowercase letter.")
        if not any(char.isdigit() for char in value):
            raise serializers.ValidationError("The password must contain at least one digit.")
        if not any(char in ['!', '@', '#', '$', '%', '^', '&', '*', '(', ')', '-', '_', '+', '=', '{', '}', '[', ']', '|', ':', ';', '"', "'", '<', '>', ',', '.', '?', '/'] for char in value):
            raise serializers.ValidationError("The password must contain at least one special character.")

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data["username"],
            password=validated_data["password"],
        )
        refresh = RefreshToken.for_user(user)

        # Create and store confirmation code for email verification
        user.confirmation_code = str(refresh.access_token)
        user.code_expires_at = datetime.datetime.now() + datetime.timedelta(minutes=60)

        user.save()


        return user
        #return User.objects.create_user(**validated_data)

class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        username = attrs.get("username")
        password = attrs.get("password")

        if username and password:
            user = authenticate(username=username, password=password)

            if not user:
                raise AuthenticationFailed("Invalid credentials")

            if not user.is_active:
                raise AuthenticationFailed("User is inactive")

            refresh = RefreshToken.for_user(user)
            return {
                "access_token": str(refresh.access_token),
                "refresh_token": str(refresh),
            }
        else:
            raise AuthenticationFailed("Must include username and password")


