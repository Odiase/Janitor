# authentication_app/tests.py

from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from django.urls import reverse

class ArtisanProfileTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)  # Ensure the client is authenticated

    def test_create_artisan_profile(self):
        url = reverse('artisan-profile-create')  # Use the name of the URL pattern
        data = {
            # "profile_image": "",
            "phone_number": "1234567890",
            "bio": "This is a test bio",
            "bio_headline": "Test Artisan",
            "preferences": {},
            "verification_status": False,
            "facebook_link": "https://facebook.com/test",
            "address": "123 Test Street",
            "latitude": 12.345678,
            "longitude": 98.765432
        }
        response = self.client.post(url, data, format='json')
        print(response.content)  # Print response content for debugging
        self.assertEqual(response.status_code, 201)
