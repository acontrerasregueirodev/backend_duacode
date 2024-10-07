# Actualización del Backend

Para actualizar el backend, sigue estos pasos:

1. **Sustituir la carpeta del entorno virtual**:
   - Reemplaza la carpeta `entorno_virtual` por la que has descargado y descomprimido.

2. **Eliminar la base de datos**:
   - Dirígete a `entorno_virtual\proyecto_duacode\db.sqlite3` y elimínala.

3. **Eliminar archivos temporales**:
   - Borra los ficheros en `entorno_virtual\proyecto_duacode\media\generar_empleados`.

4. **Ejecutar comandos de gestión**:
   - Desde `entorno_virtual\proyecto_duacode`, ejecuta los siguientes comandos:

   ```bash
   python manage.py makemigrations      # Esto prepara la BBDD
   python manage.py migrate             # Con esto la creamos
   python manage.py createsuperuser     # Crear admin de BBDD (poder tocar la BBDD desde localhost:8000/admin)
   python manage.py generar_empleados    # Ejecuta el script que carga datos en la BBDD (fotos, datos de empleados, etc.)
   python manage.py runserver           # Lanza el servidor backend




5. **Como lanzar el servidor backend-django:**

   C:\Users\Propietario\Desktop\Duacode\Proyecto Duacode\Backend\entorno_virtual\proyecto_duacode> python manage.py runserver

6. **Creación de datos en la BBDD ejecutar:**
   Ejecuta el script generar_empleados.py entorno_virtual/proyecto_duacode
    "python manage.py generar_empleados"


7. **Notas Panel de administración Django**
 acceso : 127.0.0.1:8000/admin
 user y password : propietario/duacode


  
    