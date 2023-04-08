from django.db.models import Avg
from django.test import TestCase, Client
from django.urls import reverse
from .models import Location, Player
from .serializers import LocationSerializer, PlayerMaxReport
from rest_framework import status


class FilterTestCase(TestCase):
    def setUp(self):
        Location.objects.create(location_name="Cosmodrome1", enemy_type="Fallen1", min_level=1, nr_public_events=4,
                                nr_lost_sectors=3)
        Location.objects.create(location_name="Cosmodrome2", enemy_type="Fallen2", min_level=3, nr_public_events=4,
                                nr_lost_sectors=3)
        Location.objects.create(location_name="Cosmodrome3", enemy_type="Fallen3", min_level=7, nr_public_events=4,
                                nr_lost_sectors=3)
        Location.objects.create(location_name="Cosmodrome4", enemy_type="Fallen4", min_level=9, nr_public_events=4,
                                nr_lost_sectors=3)
        Location.objects.create(location_name="Cosmodrome5", enemy_type="Fallen5", min_level=2, nr_public_events=4,
                                nr_lost_sectors=3)

    def test_location_filter(self):
        # get API response
        client = Client()
        response = client.get(reverse('location_filter', kwargs={'val': 5}))
        # get data from db
        locations_filtered = Location.objects.all().filter(min_level__gt=5)
        serializer = LocationSerializer(locations_filtered, many=True)

        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_report(self):
        # get API response
        client = Client()
        response = client.get(reverse('report_player_avg_weapons'))
        # get data from db
        queryset = Player.objects.all().annotate(avg_weapon_dmg=Avg('weapon__weapon_damage')).order_by('-avg_weapon_dmg')
        serializer = PlayerMaxReport(queryset, many=True)

        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

