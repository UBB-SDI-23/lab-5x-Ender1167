from django.db.models import Avg, Count

from .models import Weapon, Player

def report1():
    data = []
    queryset = Player.objects.all().annotate(num_weapons=Count('weapon')).order_by('-num_weapons')[:5]
    data = queryset
    return data




