from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsAdminOrModerator(BasePermission):
    """
    Доступ только для админа или модератора.
    """
    def has_permission(self, request, view):
        user = request.user
        return user.is_authenticated and user.role and user.role.name in ["Администратор", "Модератор"]


class IsSenderOrAdminModerator(BasePermission):
    """
    Чтение разрешено только отправителю и модераторам/админам.
    Изменение — только админ/модератор.
    """
    def has_object_permission(self, request, view, obj):
        user = request.user

        # Чтение (GET, HEAD, OPTIONS)
        if request.method in SAFE_METHODS:
            return obj.sender == user or (
                user.role and user.role.name in ["Администратор", "Модератор"]
            )

        # Изменение — только админ или модератор
        return user.role and user.role.name in ["Администратор", "Модератор"]
