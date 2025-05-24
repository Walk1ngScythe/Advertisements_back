from rest_framework.permissions import BasePermission


class AuthorOrAdminPermission(BasePermission):
    """
    Разрешает доступ автору объявления или пользователю с ролью admin/superadmin.
    """

    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        is_author = obj.author == request.user
        is_admin = getattr(request.user.role, "role", "") in ["admin", "superadmin"]
        return is_author or is_admin
