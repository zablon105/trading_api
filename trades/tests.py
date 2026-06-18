from django.test import TestCase
from django.urls import reverse


class HealthEndpointTest(TestCase):
    def test_health_check_returns_ok(self):
        url = reverse('health-check')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'status': 'ok', 'environment': 'production'})
