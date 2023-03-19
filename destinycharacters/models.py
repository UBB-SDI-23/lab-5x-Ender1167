from django.db import models

class Player(models.Model):
    name = models.CharField(max_length=200)
    class1 = models.CharField(max_length=200)
    level = models.IntegerField()
    glimmer = models.IntegerField()
    shards = models.IntegerField()

    def __str__(self):
        return f"{self.name} {self.class1}"


class Weapon(models.Model):

    weapon_name = models.CharField(max_length=200)
    weapon_slot = models.CharField(max_length=200)
    weapon_element = models.CharField(max_length=200)
    weapon_type = models.CharField(max_length=200)
    weapon_damage = models.IntegerField()
    player_weapon = models.ForeignKey(Player, on_delete=models.CASCADE, default=None)

    def __unicode__(self):
        return self.weapon_name

    def __str__(self):
        return f"{self.weapon_name} {self.weapon_slot}"


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
    wep = models.ForeignKey(Weapon, on_delete=models.CASCADE, default=None)
    loc = models.ForeignKey(Location, on_delete=models.CASCADE, default=None)
