# Actualización del Backend

Para actualizar el backend, sigue estos pasos:

1. **Ejecutar comandos de gestión**:
   - Desde `\proyecto_duacode`, ejecuta los siguientes comandos:

   ```bash
   python manage.py makemigrations      # Esto prepara la BBDD
   python manage.py migrate             # Con esto la creamos
   python manage.py createsuperuser     # Crear admin de BBDD (poder tocar la BBDD desde localhost:8000/admin)
   python manage.py generar_empleados   # Ejecuta el script que carga datos en la BBDD (fotos, datos de empleados, etc.)
   python manage.py runserver           # Lanza el servidor backend


2. **Como lanzar el servidor backend-django:**

   C:\Users\Propietario\Desktop\Duacode\Proyecto Duacode\Backend\proyecto_duacode> python manage.py runserver

3. **Creación de datos en la BBDD ejecutar:**

   Ejecuta el script generar_empleados.py /proyecto_duacode
    "python manage.py generar_empleados"


4. **Notas Panel de administración Django**

   acceso : 127.0.0.1:8000/admin
   user y password : los que hayais puesto al hacer createsuperuser


  
