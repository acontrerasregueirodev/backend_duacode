from django.db import models

class CodigoQR(models.Model):
    nombre = models.CharField(max_length=100)
    qr_image = models.ImageField(upload_to='codigo_qr/', blank=True)

    def __str__(self):
        return self.nombre

class CodigoEscaneado(models.Model):
    codigo = models.CharField(max_length=255)
    fecha_escaneo = models.DateTimeField(auto_now_add=True)
    usuario = models.CharField(max_length=100, blank=True)  # Opcional, para registrar quién escaneó

    def __str__(self):
        return f"{self.codigo} escaneado el {self.fecha_escaneo}"
