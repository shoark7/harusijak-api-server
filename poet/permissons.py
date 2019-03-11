from rest_framework.permissions import BasePermission, SAFE_METHODS
from rest_framework import permissions


class IsOneself(BasePermission):
    message = {'error': "본인만 작업할 수 있습니다."}

    def has_object_permission(self, request, view, obj):
        return obj.pk == request.user.pk


class IsOneselfOrReadOnly(BasePermission):
    message = {'error': "본인만 수정할 수 있습니다."}

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return obj.pk == request.user.pk


class ReadOnly(BasePermission):
    message = {'error': "읽기 전용입니다."}

    def has_permission(self, request, view):
        return request.method in SAFE_METHODS
