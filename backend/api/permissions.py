from rest_framework.permissions import BasePermission


class ReadOnlyOrAdmin(BasePermission):
    """
    Authenticated users may list and retrieve; every other action
    (create, update, delete, CSV import/export) is restricted to staff.

    Decided by viewset action rather than HTTP method, so that GET-based
    custom actions such as CSV exports stay admin-only.
    """
    read_actions = ('list', 'retrieve')

    def has_permission(self, request, view):
        user = request.user
        if not (user and user.is_authenticated):
            return False
        if getattr(view, 'action', None) in self.read_actions:
            return True
        return bool(user.is_staff)
