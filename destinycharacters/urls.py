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
from django.urls import path, re_path
from rest_framework import permissions

from .views import player_list_no_weapons, player_detail, location_list, player_list, location_detail, location_filter, \
    weapon_list, MyTokenObtainPairView
from .views import weapon_detail, Player_Weapons, location_weapon_list, report1, location_weapon_detail, player_add_weapons
#from .views import MyTokenObtainPairView, get_profile

from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from rest_framework_simplejwt import views as jwt_views

schema_view = get_schema_view(
    openapi.Info(
        title="Destiny Characters API",
        default_version='v1',
        description="API DOC",
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)
# ends here

urlpatterns = [
    re_path(r'^doc(?P<format>\.json|\.yaml)$',
            schema_view.without_ui(cache_timeout=0), name='schema-json'),  # <-- Here
    path('doc/', schema_view.with_ui('swagger', cache_timeout=0),
         name='schema-swagger-ui'),  # <-- Here
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0),
         name='schema-redoc'),  # <-- Here
    path('admin/', admin.site.urls),
    path('players/', player_list),
    path('weapons/', weapon_list),
    path('weapons/<int:pk>', weapon_detail),
    path('players/<int:pk>', player_detail),
    path('players/<int:pk>/weapons', player_add_weapons),
    path('location/', location_list, name='locations'),
    path('location/<int:pk>', location_detail),
    path('location/filter/<int:val>', location_filter, name='location_filter'),
    path('weapon_location/', location_weapon_list),
    path('weapon_location/<int:pk>', location_weapon_detail),
    path('report/', report1, name='report_player_avg_weapons'),
    path('register/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
    #path('profile/', get_profile),
]
