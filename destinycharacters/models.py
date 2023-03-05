from django.db import models


class Player(models.Model):
    name = models.CharField(max_length=200)
    class1 = models.CharField(max_length=200)
    level = models.IntegerField()
    glimmer = models.IntegerField()
    shards = models.IntegerField()

    def __str__(self):
        return self.name + "/" + self.class1
