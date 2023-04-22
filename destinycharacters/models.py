from django.db import models
from rest_framework import status
from rest_framework.response import Response


class Player(models.Model):

    Hunter = "Hunter"
    Titan = "Titan"
    Warlock = "Warlock"

    CLASS_CHOICES = [
        (Hunter, "Hunter"),
        (Titan, "Titan"),
        (Warlock, "Warlock")
    ]
    name = models.CharField(max_length=200)
    class1 = models.CharField(max_length=200, choices=CLASS_CHOICES, default=Hunter)
    level = models.IntegerField()
    glimmer = models.IntegerField()
    shards = models.IntegerField()

    def __str__(self):
        return f"{self.name} {self.class1}"


class Weapon(models.Model):

    Void = "Void"
    Solar = "Solar"
    Arc = "Arc"
    Stasis = "Stasis"
    Strand = "Strand"
    Kinetic = "Kinetic"

    ELEMENT_CHOICES = [
        (Void, "Void"),
        (Solar, "Solar"),
        (Arc, "Arc"),
        (Stasis, "Stasis"),
        (Strand, "Strand"),
        (Kinetic, "Kinetic")
    ]
    SLOT_CHOICES = [
        ("Kinetic", "Kinetic"),
        ("Energy", "Energy"),
        ("Heavy", "Heavy")
    ]

    weapon_name = models.CharField(max_length=200)
    weapon_slot = models.CharField(max_length=200, choices=SLOT_CHOICES, default=Kinetic)
    weapon_element = models.CharField(max_length=200, choices=ELEMENT_CHOICES, default=Void)
    weapon_type = models.CharField(max_length=200)
    weapon_damage = models.IntegerField()
    weapon_description = models.TextField(blank=True, null=True)
    player_weapon = models.ForeignKey(Player, on_delete=models.CASCADE, default=None)

    def __unicode__(self):
        return self.weapon_name

    def __str__(self):
        return f"{self.weapon_name} {self.weapon_slot}"

    def create(self, request, pk=None, company_pk=None, project_pk=None):
        is_many = isinstance(request.data, list)

        serializer = self.get_serializer(data=request.data, many=is_many)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class Location(models.Model):

    location_name = models.CharField(max_length=200)
    enemy_type = models.CharField(max_length=200)
    min_level = models.IntegerField()
    nr_public_events = models.IntegerField()
    nr_lost_sectors = models.IntegerField()
    all_weapons = models.ManyToManyField(Weapon, through='Location_Weapon')

    def __str__(self):
        return f"{self.location_name} {self.enemy_type}"


class Location_Weapon(models.Model):

    drop_rate = models.IntegerField()
    wep = models.ForeignKey(Weapon, on_delete=models.CASCADE, default=None, null=True)
    loc = models.ForeignKey(Location, on_delete=models.CASCADE, default=None, null=True)
