from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse

class PanelEmpleadosViewTests(TestCase):
    def setUp(self):
        # Crea un usuario de prueba y loguéalo
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.login(username='testuser', password='testpassword')

    def test_panel_empleados_view(self):
        # Realiza la solicitud GET a la vista
        response = self.client.get(reverse('panel-empleados'))
        self.assertEqual(response.status_code, 200)  # Verifica que la respuesta sea 200
        # Puedes verificar el contenido de la respuesta
        # self.assertContains(response, "mensaje")  # Cambia "mensaje" al conten