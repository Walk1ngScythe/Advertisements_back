from rest_framework import viewsets

from app_auth.permissions import AuthorOrAdminPermission


class BaseEditViewSet(viewsets.ModelViewSet):
    permission_classes = [AuthorOrAdminPermission]
