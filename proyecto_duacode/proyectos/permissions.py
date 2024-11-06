from rest_framework.permissions import BasePermission

class IsAuthenticatedToDelete(BasePermission):
    """
    Permiso personalizado para permitir que solo los usuarios autenticados puedan eliminar proyectos.
    """

    def has_permission(self, request, view):
        # Permitir el acceso si es un método seguro (GET, POST, PUT, PATCH) y si el usuario está autenticado
        if request.method in ['GET', 'POST', 'PUT', 'PATCH']:
            return True
        
        # Permitir la eliminación solo si el usuario está autenticado
        if request.method == 'DELETE' and request.user.is_authenticated:
            return True
        
        # Si no se cumple la condición, denegar el acceso
        return False
