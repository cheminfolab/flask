from rest_framework.permissions import SAFE_METHODS, BasePermission


class CompoundUserWritePermission(BasePermission):
    message = 'Editing compounds is restricted to the creator and admins.'

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return obj.created_by == request.user

