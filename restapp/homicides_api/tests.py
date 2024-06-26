from django.test import TestCase
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.urls import reverse
from homicides_api.models import *

class HomicideTests(APITestCase):
    def setUp(self):
        self.client = APIClient()
        # Create test data
        self.victim = Victim.objects.create(race="Asian", age=30, sex="Male")
        self.location = Location.objects.create(city="Test City", state="Test State")
        self.disposition = Disposition.objects.create(disposition="Closed by arrest")
        self.homicide = Homicide.objects.create(
            victim=self.victim, location=self.location, disposition=self.disposition, date="2020-02-20"
        )
        self.valid_payload = {
                'victim': {
                    'race': 'Black', 'age': 25, 'sex': 'Female'
                },
                'location': {
                    'city': 'New City', 'state': 'New State'
                },
                'disposition': {
                    'disposition': 'Open/No arrest'
                },
                'date': '2021-01-01'
            }
        self.invalid_payload = {
                'victim': {},  # Invalid data
                'location': {},
                'disposition': {},
                'date': ''
            }

    def test_get_all_homicides(self):
        # Reverse Function: The reverse function is used to dynamically generate the URL for the view. 
        # This helps to avoid hardcoding URLs and makes the tests more robust to URL changes.
        response = self.client.get(reverse('homicide-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_homicides_by_race(self):
        response = self.client.get(reverse('homicide-get-by-victim-race') + '?race=Asian')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)

    def test_get_homicides_by_gender_age_range(self):
        response = self.client.get(reverse('homicide-get-by-gender-age-range') + '?gender=Male&min_age=20&max_age=40')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)

    def test_get_homicides_count_by_city(self):
        response = self.client.get(reverse('homicide-get-homicides-count-by-city'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)

    def test_create_homicide(self):
        response = self.client.post(reverse('homicide-list'), data=self.valid_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_update_homicide(self):
        response = self.client.put(
            reverse('homicide-detail', kwargs={'pk': self.homicide.pk}),
            data=self.valid_payload,
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_homicide(self):
        response = self.client.delete(reverse('homicide-detail', kwargs={'pk': self.homicide.pk}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
