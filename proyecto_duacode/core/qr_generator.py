# qr_generator.py
import qrcode
from io import BytesIO
from django.core.files import File

def generate_qr_code(employee):
    # Generar el contenido del QR (en este caso un JSON con la información del empleado)
    qr_content = f"""
    {{
        "id": {employee.id},
        "nombre": "{employee.nombre}",
        "apellido_1": "{employee.apellido_1}",
        "apellido_2": "{employee.apellido_2}",
        "email": "{employee.email}",
        "puesto": "{employee.rol.nombre}",
        "sede": "{employee.sede.nombre if employee.sede else 'No asignada'}"
    }}
    """
    
    # Crear el código QR
    qr_image = qrcode.make(qr_content)
    
    # Guardar el código QR en un archivo temporal
    qr_io = BytesIO()
    qr_image.save(qr_io, format='PNG')
    qr_file = File(qr_io, name=f'{employee.nombre}_{employee.apellido_1}_{employee.apellido_2}qr.png')
    
    return qr_file
