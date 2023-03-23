"""destinycharacters URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path
from .views import player_list_no_weapons, player_detail, location_list, location_detail, location_filter,weapon_list
from .views import weapon_detail, Player_Weapons, location_weapon_list, report1, location_weapon_detail, player_list

urlpatterns = [
    path('admin/', admin.site.urls),
    path('players/', player_list),
    path('weapons/', weapon_list),
    path('weapons/<int:pk>', weapon_detail),
    path('players/<int:pk>', player_detail),
    path('location/', location_list),
    path('location/<int:pk>', location_detail),
    path('location/filter/<int:val>', location_filter),
    path('weapon_location/', location_weapon_list),
    path('weapon_location/<int:pk>', location_weapon_detail),
    path('report/', report1),

]
