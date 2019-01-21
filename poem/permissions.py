from rest_framework import permissions


class IsWriterOrReadOnly(permissions.BasePermission):
    message = {'error': "작성한 본인만 작업할 수 있습니다."}

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.writer == request.user
