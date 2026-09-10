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

_STATUS_CODES = {
    "VALIDATION_ERROR": status.HTTP_400_BAD_REQUEST,
    "UNAUTHENTICATED": status.HTTP_401_UNAUTHORIZED,
    "PERMISSION_DENIED": status.HTTP_403_FORBIDDEN,
    "NOT_FOUND": status.HTTP_404_NOT_FOUND,
    "METHOD_NOT_ALLOWED": status.HTTP_405_METHOD_NOT_ALLOWED,
    "THROTTLED": status.HTTP_429_TOO_MANY_REQUESTS,
}


def _resolve_code(exc):
    for exc_type, code in _EXCEPTION_CODES.items():
        if isinstance(exc, exc_type):
            return code
    return "ERROR"


def _extract_details(exc):
    detail = getattr(exc, "detail", None)
    if isinstance(detail, dict):
        return detail
    if isinstance(detail, list):
        return {"non_field_errors": [str(item) for item in detail]}
    if detail is not None:
        return {"detail": str(detail)}
    return {}


def _is_request_authenticated(context):
    request = context.get("request")
    user = getattr(request, "user", None)
    return bool(user and getattr(user, "is_authenticated", False))


def custom_exception_handler(exc, context):
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

    if code == "PERMISSION_DENIED" and not _is_request_authenticated(context):
        code = "UNAUTHENTICATED"

    response.status_code = _STATUS_CODES.get(code, response.status_code)
    response.data = {
        "code": code,
        "message": _DEFAULT_MESSAGES.get(code, "The request could not be processed."),
        "details": _extract_details(exc),
    }
    return response