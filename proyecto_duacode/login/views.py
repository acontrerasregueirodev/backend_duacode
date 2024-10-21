
from django.shortcuts import redirect
from django.contrib.auth import authenticate, login, logout

from django.http import JsonResponse


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            welcome_message = f"Bienvenido, {user.username} {user.id}!"  # Mensaje de bienvenida
            return JsonResponse({'message': user.id})
        
        else:
            return JsonResponse({'message': "Credenciales incorrectas. Inténtalo de nuevo."}, status=400)

    return JsonResponse({'message': "Método no permitido."}, status=405)

def logout_view(request):
    logout(request)
    return JsonResponse({'message': "Has sido desconectado."})