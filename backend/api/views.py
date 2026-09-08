from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response


@api_view(["GET"])
def health(request):
    return Response({"message": "Django API is running healthy!"})


def not_found(request, exception=None):
    """
    Django's handler404, used for requests that don't match any URL pattern
    at all (so they never reach a DRF view and never pass through
    api.exceptions.custom_exception_handler). Kept in the same JSON shape
    for a consistent error contract across the whole API.

    Note: Django only invokes this when DEBUG=False. With DEBUG=True it
    shows its own technical 404 debug page instead — see the QA checklist.
    """
    return JsonResponse(
        {
            "code": "NOT_FOUND",
            "message": "The requested resource was not found.",
            "details": {},
        },
        status=404,
    )
