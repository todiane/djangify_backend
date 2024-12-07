from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from .models import Contact

class ContactAPITest(TestCase):
    def setUp(self):
        # This runs before each test
        self.client = APIClient()
        self.url = reverse('contact-messages-list')  # This will get your API endpoint URL

    def test_valid_contact_submission(self):
        # Test data
        data = {
            "name": "Test User",
            "email": "test@example.com",
            "message": "This is a test message that needs to be at least 10 characters",
            "contact_reason": "other"
        }
        
        # Make the POST request
        response = self.client.post(self.url, data, format='json')
        
        # Print response details for debugging
        print(f"Status Code: {response.status_code}")
        print(f"Response Data: {response.data}")
        
        # Assertions
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Contact.objects.filter(email="test@example.com").exists())

    def test_invalid_email(self):
        data = {
            "name": "Test User",
            "email": "invalid-email",  # Invalid email format
            "message": "This is a test message that needs to be at least 10 characters",
            "contact_reason": "other"
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_short_message(self):
        data = {
            "name": "Test User",
            "email": "test@example.com",
            "message": "short",  # Too short
            "contact_reason": "other"
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)