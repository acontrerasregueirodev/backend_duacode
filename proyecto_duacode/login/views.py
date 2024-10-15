from django.contrib.auth import authenticate, login
from django.shortcuts import render

def login_view(request):
    print("CSRF Token:", request.META.get('CSRF_COOKIE'))
    welcome_message = ""  # Initialize the welcome message

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            
            welcome_message = f"Bienvenido, {user.username}!"  # Set the welcome message
        else:
            welcome_message = "Credenciales incorrectas. Inténtalo de nuevo."  # Handle invalid login

    return render(request, 'login/login.html', {'welcome_message': welcome_message})  # Pass the message to the template
