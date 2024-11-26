from django.db import migrations

def create_roles(apps, schema_editor):
    RolModel = apps.get_model('core', 'RolModel')

    # Crear roles
    ceo = RolModel.objects.create(nombre="CEO")
    cto = RolModel.objects.create(nombre="CTO")
    lider_desarrollo = RolModel.objects.create(nombre="LÍDER_DESARROLLO")
    ingeniero_frontend = RolModel.objects.create(nombre="INGENIERO_FRONTEND")
    ingeniero_backend = RolModel.objects.create(nombre="INGENIERO_BACKEND")
    lider_qa = RolModel.objects.create(nombre="LÍDER_QA")
    ingeniero_qa = RolModel.objects.create(nombre="INGENIERO_QA")
    gerente_proyecto = RolModel.objects.create(nombre="GERENTE_PROYECTO")
    coordinador_proyecto = RolModel.objects.create(nombre="COORDINADOR_PROYECTO")
    cfo = RolModel.objects.create(nombre="CFO")
    gerente_producto = RolModel.objects.create(nombre="GERENTE_PRODUCTO")
    propietario_producto = RolModel.objects.create(nombre="PROPIETARIO_PRODUCTO")
    gerente_marketing = RolModel.objects.create(nombre="GERENTE_MARKETING")
    especialista_marketing = RolModel.objects.create(nombre="ESPECIALISTA_MARKETING")
    gerente_ventas = RolModel.objects.create(nombre="GERENTE_VENTAS")
    representante_ventas = RolModel.objects.create(nombre="REPRESENTANTE_VENTAS")
    gerente_soporte = RolModel.objects.create(nombre="GERENTE_SOPORTE")
    especialista_soporte = RolModel.objects.create(nombre="ESPECIALISTA_SOPORTE")

    # Establecer las jerarquías
    ceo.supervisa_a.add(cto, cfo, gerente_producto, gerente_marketing, gerente_ventas, gerente_soporte)
    cto.supervisa_a.add(lider_desarrollo, lider_qa, gerente_proyecto)
    lider_desarrollo.supervisa_a.add(ingeniero_frontend, ingeniero_backend)
    lider_qa.supervisa_a.add(ingeniero_qa)
    gerente_producto.supervisa_a.add(propietario_producto)
    gerente_marketing.supervisa_a.add(especialista_marketing)
    gerente_ventas.supervisa_a.add(representante_ventas)
    gerente_soporte.supervisa_a.add(especialista_soporte)

    # Guardar cambios
    ceo.save()
    cto.save()
    lider_desarrollo.save()
    ingeniero_frontend.save()
    ingeniero_backend.save()
    lider_qa.save()
    ingeniero_qa.save()
    gerente_proyecto.save()
    coordinador_proyecto.save()
    cfo.save()
    gerente_producto.save()
    propietario_producto.save()
    gerente_marketing.save()
    especialista_marketing.save()
    gerente_ventas.save()
    representante_ventas.save()
    gerente_soporte.save()
    especialista_soporte.save()

class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),  # Ajusta esto según el nombre de tu última migración
    ]

    operations = [
        migrations.RunPython(create_roles),
    ]