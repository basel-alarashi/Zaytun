import logging

from django.core.exceptions import PermissionDenied as DjangoPermissionDenied
from django.http import Http404
from rest_framework import status
from rest_framework.exceptions import (
    AuthenticationFailed,
    MethodNotAllowed,
    NotAuthenticated,
    NotFound,
    PermissionDenied,
    Throttled,
    ValidationError,
)
from rest_framework.response import Response
from rest_framework.views import exception_handler as drf_exception_handler

logger = logging.getLogger(__name__)

# Order matters only in that every exception type here is mutually exclusive
# in practice, so a plain dict lookup by isinstance() is sufficient.
_EXCEPTION_CODES = {
    ValidationError: "VALIDATION_ERROR",
    NotAuthenticated: "UNAUTHENTICATED",
    AuthenticationFailed: "UNAUTHENTICATED",
    PermissionDenied: "PERMISSION_DENIED",
    DjangoPermissionDenied: "PERMISSION_DENIED",
    NotFound: "NOT_FOUND",
    Http404: "NOT_FOUND",
    MethodNotAllowed: "METHOD_NOT_ALLOWED",
    Throttled: "THROTTLED",
}

_DEFAULT_MESSAGES = {
    "VALIDATION_ERROR": "The request could not be processed.",
    "UNAUTHENTICATED": "Authentication is required to access this resource.",
    "PERMISSION_DENIED": "You do not have permission to perform this action.",
    "NOT_FOUND": "The requested resource was not found.",
    "METHOD_NOT_ALLOWED": "This method is not allowed for this endpoint.",
    "THROTTLED": "Too many requests. Please try again later.",
    "SERVER_ERROR": "An unexpected error occurred.",
}


def _resolve_code(exc):
    for exc_type, code in _EXCEPTION_CODES.items():
        if isinstance(exc, exc_type):
            return code
    return "ERROR"


def _extract_details(exc):
    """Best-effort extraction of field-level details from DRF's exception data."""
    detail = getattr(exc, "detail", None)
    if isinstance(detail, dict):
        return detail
    if isinstance(detail, list):
        return {"non_field_errors": [str(item) for item in detail]}
    if detail is not None:
        return {"detail": str(detail)}
    return {}


def custom_exception_handler(exc, context):
    """
    Reshape every API error response into Zaytun's canonical error contract:

        {"code": "...", "message": "...", "details": {...}}

    (see 10_API_Specification.md §12).

    Exceptions DRF itself doesn't recognize (i.e. anything that isn't an
    APIException/Http404/Django PermissionDenied) fall through to a safe,
    non-leaking 500 response, and are logged server-side so they remain
    diagnosable (NFR-011) without exposing internals to the client.
    """
    response = drf_exception_handler(exc, context)

    if response is None:
        logger.exception(
            "Unhandled exception in view %s", context.get("view"), exc_info=exc
        )
        return Response(
            {
                "code": "SERVER_ERROR",
                "message": _DEFAULT_MESSAGES["SERVER_ERROR"],
                "details": {},
            },
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )

    code = _resolve_code(exc)
    response.data = {
        "code": code,
        "message": _DEFAULT_MESSAGES.get(code, "The request could not be processed."),
        "details": _extract_details(exc),
    }
    return response
