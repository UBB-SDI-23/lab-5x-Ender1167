from rest_framework import serializers
from .models import Player
from .models import Weapon
from .models import Location
from .models import Location_Weapon

class WeaponSerializer(serializers.ModelSerializer):

    class Meta:
        model = Weapon
        fields = ['id', 'weapon_name', 'weapon_slot', 'weapon_element', 'weapon_type', 'weapon_damage', 'player_weapon']


class Location_WeaponSerializer(serializers.ModelSerializer):

    class Meta:
        model = Location_Weapon
        fields = ['id', 'drop_rate', 'wep', 'loc']
        depth = 1

class WeaponSerializerIds(serializers.ModelSerializer):

    class Meta:
        model = Weapon
        fields = ['id']


class PlayerSerializer(serializers.ModelSerializer):
    weapons = WeaponSerializer(source='weapon_set', many=True)

    class Meta:
        model = Player
        fields = ['id', 'name', 'class1', 'level', 'glimmer', 'shards', 'weapons']


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
    max_nr_weapons = serializers.SerializerMethodField()

    class Meta:
        model = Player
        fields = ['max_nr_weapons', 'name', 'class1', 'level', 'glimmer', 'shards']

    def get_max_nr_weapons(self, obj):
        max_nr_wep = self.context.get("max_nr_weapons")
        return max_nr_wep



