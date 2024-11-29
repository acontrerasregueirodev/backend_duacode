from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework_simplejwt.tokens import RefreshToken

class LoginView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            # Generar tokens JWT
            refresh = RefreshToken.for_user(user)
            return Response({
                'access': str(refresh.access_token),
                'refresh': str(refresh),
                'user_id': user.id,
                'username': user.username,
            })

        return Response({'message': "Credenciales incorrectas. Inténtalo de nuevo."}, status=400)

class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        username = request.user.username
        logout(request)
        return Response({'message': f"{username} ha cerrado sesión correctamente."}, status=200)

class CheckLoginView(APIView):
    permission_classes = [IsAuthenticated]  # Requiere autenticación JWT

    def get(self, request):
        return Response({
            "message": "Estás autenticado",
            "user_id": request.user.id,
            "username": request.user.username,
        }, status=200)
