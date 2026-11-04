from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsOwnerOrEditFieldOnly(BasePermission):
    """
    Object-level permission for containers.

    Staff and members of the owning working group may edit every field.
    Everyone else may only update the fields listed in `fields`.
    A container without an owner counts as owned by nobody: users without
    a working group are *not* treated as members of it.
    """
    fields = ('amount_left',)
    message = (
        f"Editing containers (exceptions: {list(fields)}) "
        "is restricted to members of the owning group."
    )

    def has_object_permission(self, request, view, obj):
        user = request.user
        if not (user and user.is_authenticated):
            return False
        if user.is_staff:
            return True
        if obj.owner_id is not None and user.working_group_id == obj.owner_id:
            return True
        return set(request.data.keys()).issubset(self.fields)


class UserWritePermission(BasePermission):
    message = 'Editing compounds is restricted to the creator.'  # and admins.'

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return obj.created_by == request.user
