from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse
from rest_framework.decorators import api_view, permission_classes

class LoginView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            print(f"Bienvenido, {user.username} {user.id}!")
            return Response({'message': user.id})
        
        return Response({'message': "Credenciales incorrectas. Inténtalo de nuevo."}, status=400)

class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        print("Intentando hacer logout")
        username = request.user.username
        logout(request)
        print(f"{username} ha cerrado sesión.")
        return Response({'message': f"{username} ha cerrado sesión."}, status=200)

class CheckLoginView(APIView):
    permission_classes = [IsAuthenticated]  # Requiere autenticación

    def get(self, request):
        print("Accediendo a check login")
        return Response({"mensaje": "Estás autenticado", 'user': request.user.username}, status=200)
