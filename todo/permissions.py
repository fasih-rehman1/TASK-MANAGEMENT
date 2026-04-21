from rest_framework.permissions import BasePermission

class IsSuperAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user.profile.role == 'superadmin'
    
class IsAdmin(BasePermission):
    def has_permission(self, request, view, obj):
        return request.user.profile.role in ['superadmin', 'admin']
    
class IsManager(BasePermission):
    def has_permission(self, request, view):
        return request.user.profile.role in ['superadmin', 'admin', 'manager']
    
class IsUser(BasePermission):
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        return request.user.profile.role in ['superadmin', 'admin', 'manager', 'user']