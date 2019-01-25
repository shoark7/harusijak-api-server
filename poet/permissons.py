from rest_framework import permissions


class IsOneself(permissions.BasePermission):
    message = {'error': "본인만 작업할 수 있습니다."}

    def has_object_permission(self, request, view, obj):
        return obj.pk == request.user.pk


class IsOneselfOrReadOnly(permissions.BasePermission):
    message = {'error': "본인만 수정할 수 있습니다."}

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.pk == request.user.pk
