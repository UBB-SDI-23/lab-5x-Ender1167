from django.contrib.auth.base_user import BaseUserManager
from django.db import models
from rest_framework import status
from rest_framework.response import Response
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractUser

def validateAge(value):
    if value < 0:
        raise ValidationError(
            _("%(value)s is below 0."),
            params={"value": value},
        )

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
    #user_player = models.ForeignKey(UserProfile, on_delete=models.CASCADE, default=None)

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


def validateLostSectors(value):
    if value < 3:
        raise ValidationError(
            _("%(value)s is below 3."),
            params={"value": value},
        )

def validateMinLevel(value):
    if value < 1:
        raise ValidationError(
            _("%(value)s is below 1."),
            params={"value": value},
        )
class Location(models.Model):
    enemy_default = 'Fallen'
    ENEMY_CHOICES = [
        ("Fallen", "Fallen"),
        ("Scorn", "Scorn"),
        ("Cabal", "Cabal"),
        ("Vex", "Vex"),
        ("Taken", "Taken")
    ]

    location_name = models.CharField(max_length=200)
    enemy_type = models.CharField(max_length=200, choices=ENEMY_CHOICES, default=enemy_default)
    min_level = models.IntegerField(validators=[validateMinLevel])
    nr_public_events = models.IntegerField()
    nr_lost_sectors = models.IntegerField(validators=[validateLostSectors])
    all_weapons = models.ManyToManyField(Weapon, through='Location_Weapon')

    def __str__(self):
        return f"{self.location_name} {self.enemy_type}"


class Location_Weapon(models.Model):

    drop_rate = models.IntegerField()
    wep = models.ForeignKey(Weapon, on_delete=models.CASCADE, default=None, null=True)
    loc = models.ForeignKey(Location, on_delete=models.CASCADE, default=None, null=True)


class CustomUserManager(BaseUserManager):
    def create_user(self, username, password, **extra_fields):
        """
        Creates and saves a User with the given username and password.
        """
        if not username:
            raise ValueError('The Username field must be set')

        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        print(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password=None, **extra_fields):
        """
        Creates and saves a superuser with the given username and password.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(username, password, **extra_fields)



class UserProfile(AbstractUser):
    not_married = "Not married"
    MALE = "Male"
    FEMALE = "Female"
    MARITAL_CHOICES = [
        ("Married", "Married"),
        ("Not married", "Not married")
    ]
    GENDER_CHOICES = [
        (MALE, "Male"),
        (FEMALE, "Female")
    ]

    #user = models.OneToOneField(User, related_name='profile', on_delete=models.CASCADE)
    bio = models.TextField(max_length=500, blank=True, null=True)
    location = models.CharField(max_length=30, blank=True, null=True)
    age = models.IntegerField(validators=[validateAge], null=True)
    gender = models.CharField(max_length=30, choices=GENDER_CHOICES, default=MALE, blank=True, null=True)
    marital_status = models.CharField(max_length=30, choices=MARITAL_CHOICES, default=not_married, blank=True, null=True)

    object = CustomUserManager()