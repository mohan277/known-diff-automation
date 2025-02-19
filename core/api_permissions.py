from rest_framework.permissions import BasePermission
from .encryption import (jwt_decode_handler, crypto_decode)
from account.models import Users


class UserAuthentication(BasePermission):
    """
    Allows access only to authenticated users.
    """

    def has_permission(self, request, view):
        try:
            user_id = crypto_decode(
                jwt_decode_handler(
                    request.COOKIES['token']
                )['user_id']
            )
            request.user = Users.objects.get(id=int(
                user_id))
            return True
        except Exception as e:
            return False
