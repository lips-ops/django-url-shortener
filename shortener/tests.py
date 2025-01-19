from django.test import TestCase

# Create your tests here.
from django.test import TestCase
from django.urls import reverse


class URLShortenerTests(TestCase):

    def test_valid_url(self):
        response = self.client.post(reverse('shorten_url'), {'url': 'https://example.com'})
        self.assertEqual(response.status_code, 200)
        self.assertIn('short_url', response.json())

    def test_invalid_url(self):
        response = self.client.post(reverse('shorten_url'), {'url': 'invalid-url'})
        self.assertEqual(response.status_code, 400)
        self.assertIn('error', response.json())

    def test_url_with_password(self):
        response = self.client.post(reverse('shorten_url'), {'url': 'https://example.com', 'password': 'securepass'})
        short_url = response.json().get('short_url')

        # Test accessing with correct password
        response = self.client.get(f'/r/{short_url.split("/")[-1]}/?password=securepass')
        self.assertEqual(response.status_code, 302)  # Redirect to original URL

        # Test accessing with incorrect password
        response = self.client.get(f'/r/{short_url.split("/")[-1]}/?password=wrongpass')
        self.assertEqual(response.status_code, 403)
