from rest_framework.permissions import BasePermission, SAFE_METHODS
from django.contrib.auth import get_user_model


class IsOwnerOrEditFieldOnly(BasePermission):
    """
    Object-level permission to only allow members of object owning group to edit.
    If member is not part of owning group, editing is restricted to specific field.
    """

    def __init__(self):
        super().__init__()
        self.fields = ['amount_left', 'last_used', 'last_user']
        self.message = f"Editing containers (exceptions: {self.fields}) is restricted to members of the owning group."

    def has_object_permission(self, request, view, obj):
        if not request.user.is_authenticated:
            return False
        update_fields = [key for key in request.data]
        member = get_user_model()
        working_group = member.objects.get(pk=request.user.id).working_group
        owner = obj.owner
        if working_group != owner:
            return set(update_fields).issubset(set(self.fields))
        return True


class UserWritePermission(BasePermission):
    message = 'Editing compounds is restricted to the creator.'  # and admins.'

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return obj.created_by == request.user
