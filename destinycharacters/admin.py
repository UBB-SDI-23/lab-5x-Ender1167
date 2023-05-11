from django.contrib import admin
from .models import Player
from .models import Weapon
from .models import Location
from .models import Location_Weapon
from .models import UserProfile

admin.site.register(Player)
admin.site.register(Weapon)
admin.site.register(Location)
admin.site.register(Location_Weapon)
admin.site.register(UserProfile)
