from django.test import TestCase, Client
from django.urls import reverse
from .models import Location
from .serializers import LocationSerializer
from rest_framework import status


class FilterTestCase(TestCase):
    def setUp(self):
        Location.objects.create(location_name="Cosmodrome1", enemy_type="Fallen1", min_level=1, nr_public_events=4, nr_lost_sectors=3)
        Location.objects.create(location_name="Cosmodrome2", enemy_type="Fallen2", min_level=3, nr_public_events=4,
                                nr_lost_sectors=3)
        Location.objects.create(location_name="Cosmodrome3", enemy_type="Fallen3", min_level=7, nr_public_events=4,
                                nr_lost_sectors=3)
        Location.objects.create(location_name="Cosmodrome4", enemy_type="Fallen4", min_level=9, nr_public_events=4,
                                nr_lost_sectors=3)
        Location.objects.create(location_name="Cosmodrome5", enemy_type="Fallen5", min_level=2, nr_public_events=4,
                                nr_lost_sectors=3)

    def test_get_all_locations(self):
        # get API response
        client = Client()
        response = client.get(reverse('location/'))
        # get data from db
        locations = Location.objects.all()
        serializer = LocationSerializer(locations, many=True)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)