from rest_framework import viewsets

from app_auth.permissions import AuthorOrAdminPermission

from app_auth.permissions import IsSelfOrAdminPermission


class BaseEditViewSet(viewsets.ModelViewSet):
    permission_classes = [AuthorOrAdminPermission]

class BaseEditUserViewSet(viewsets.ModelViewSet):
    permission_classes = [IsSelfOrAdminPermission]