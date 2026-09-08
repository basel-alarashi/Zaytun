from rest_framework import status
from rest_framework.test import APITestCase


class HealthEndpointTests(APITestCase):
    def test_health_returns_200_and_expected_payload(self):
        response = self.client.get("/api/v1/health/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("message", response.data)

    def test_unsupported_method_returns_canonical_error_contract(self):
        response = self.client.post("/api/v1/health/")

        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        self.assertEqual(response.data["code"], "METHOD_NOT_ALLOWED")
        self.assertIn("message", response.data)
        self.assertIn("details", response.data)


class NotFoundHandlerTests(APITestCase):
    def test_unmatched_route_returns_json_error_when_debug_disabled(self):
        # Django only invokes handler404 when DEBUG=False; with DEBUG=True it
        # renders its own technical debug page instead.
        with self.settings(DEBUG=False, ALLOWED_HOSTS=["testserver"]):
            response = self.client.get("/api/v1/this-route-does-not-exist/")

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        payload = response.json()
        self.assertEqual(payload["code"], "NOT_FOUND")
        self.assertIn("message", payload)
