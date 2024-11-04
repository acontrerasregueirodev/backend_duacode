
from django.shortcuts import redirect
from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        print(user)
        
        if user is not None:
            login(request, user)
            print(f"Bienvenido, {user.username} {user.id}!") #) Mensaje de bienvenida
            return JsonResponse({'message': user.id})
        
        else:
            print({'message': "Credenciales incorrectas. Inténtalo de nuevo."})
            return JsonResponse({'message': "Credenciales incorrectas. Inténtalo de nuevo."}, status=400)

    return JsonResponse({'message': "Método no permitido."}, status=405)

def logout_view(request):
    print("intentando hacer logout")
    if request.user.is_authenticated:
        # Si el usuario está autenticado, realizar el logout
        username = request.user.username
        logout(request)
        
        # Comprobar si el usuario fue desconectado correctamente
        if not request.user.is_authenticated:
            print(f"{username} has been logged out.")
            return JsonResponse({'message': f"{username} has been logged out."})
        else:
            print('message Logout failed.')
            return JsonResponse({'message': "Logout failed."}, status=500)
    else:
        print('message No user is logged in.')
        return JsonResponse({'message': "No user is logged in."}, status=400)