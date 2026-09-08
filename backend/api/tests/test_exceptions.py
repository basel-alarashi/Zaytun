from django.test import SimpleTestCase
from rest_framework import status
from rest_framework.exceptions import (
    AuthenticationFailed,
    MethodNotAllowed,
    NotFound,
    PermissionDenied,
    ValidationError,
)

from api.exceptions import custom_exception_handler


class CustomExceptionHandlerTests(SimpleTestCase):
    def _context(self):
        # The default DRF handler doesn't require a real view/request for
        # the exception types exercised here.
        return {"view": None, "request": None}

    def test_validation_error_maps_to_validation_error_code(self):
        exc = ValidationError({"email": ["This field is required."]})

        response = custom_exception_handler(exc, self._context())

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["code"], "VALIDATION_ERROR")
        self.assertEqual(response.data["details"], {"email": ["This field is required."]})

    def test_authentication_failure_maps_to_unauthenticated_code(self):
        exc = AuthenticationFailed("Invalid credentials.")

        response = custom_exception_handler(exc, self._context())

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data["code"], "UNAUTHENTICATED")

    def test_permission_denied_maps_to_permission_denied_code(self):
        exc = PermissionDenied()

        response = custom_exception_handler(exc, self._context())

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.data["code"], "PERMISSION_DENIED")

    def test_not_found_maps_to_not_found_code(self):
        exc = NotFound()

        response = custom_exception_handler(exc, self._context())

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data["code"], "NOT_FOUND")

    def test_method_not_allowed_maps_to_method_not_allowed_code(self):
        exc = MethodNotAllowed("POST")

        response = custom_exception_handler(exc, self._context())

        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        self.assertEqual(response.data["code"], "METHOD_NOT_ALLOWED")

    def test_unhandled_exception_returns_safe_500_without_leaking_details(self):
        exc = RuntimeError("password=hunter2; db connection dropped")

        response = custom_exception_handler(exc, self._context())

        self.assertEqual(response.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)
        self.assertEqual(response.data["code"], "SERVER_ERROR")
        self.assertNotIn("hunter2", str(response.data))
        self.assertNotIn("db connection dropped", str(response.data))
