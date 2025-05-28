from rest_framework.permissions import BasePermission


class AuthorOrAdminPermission(BasePermission):
    """
    Разрешает доступ автору объявления или пользователю с ролью admin/superadmin.
    """

    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        role_name = getattr(request.user.role, "name", "")
        is_author = obj.author == request.user
        is_admin = role_name in ["admin", "superadmin"]
        return is_author or is_admin


class IsSelfOrAdminPermission(BasePermission):
    """
    Разрешает доступ только пользователю, который редактируется (самому себе),
    или пользователю с ролью admin/superadmin.
    """

    def has_permission(self, request, view):
        # Просто проверяем, что пользователь аутентифицирован
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        role_name = getattr(request.user.role, "name", "")
        is_self = obj == request.user
        is_admin = role_name in ["admin", "superadmin"]
        return is_self or is_admin