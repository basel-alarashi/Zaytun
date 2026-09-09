from rest_framework.authentication import SessionAuthentication as BaseSessionAuthentication


class SessionAuthentication(BaseSessionAuthentication):

    def authenticate(self, request):
        result = super().authenticate(request)
        if result is None:
            return None
        user, auth = result
        if not user.is_authenticated:
            return None
        return (user, auth)