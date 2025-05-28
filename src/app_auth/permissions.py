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
        print(f"DEBUG:: Author? {is_author} | Admin? {is_admin} | Role: {role_name}")
        return is_author or is_admin

