from rest_framework import permissions

class IsManagerOrReadOnly(permissions.BasePermission):


    def has_permission(self, request, view):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True

        elif request.method not in permissions.SAFE_METHODS  and request.user.groups.filter(name='Manager').exists():
            return True
        else: 
            return False

class IsManagerOnly(permissions.BasePermission):


    def has_permission(self, request, view):
        
        if request.user.groups.filter(name='Manager').exists():
            return True
        
        return False
