from django.db import models

class Inicio(models.Model):
    nombre_viaje = models.CharField(max_length=200)

    def __str__(self):
        return self.nombre_viaje


class Cliente(models.Model):
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    correo = models.EmailField(unique=True)
    telefono = models.CharField(max_length=20)
    cedula = models.CharField(max_length=20)
    password = models.CharField(max_length=255)  # Guardada encriptada

    def __str__(self):
        return f"{self.nombre} {self.apellido}"


class Guia(models.Model):
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    correo = models.EmailField(unique=True)
    telefono = models.CharField(max_length=20)
    cedula = models.CharField(max_length=20)
    licencia = models.CharField(max_length=100)
    poli = models.BooleanField(default=False)
    password = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.nombre} {self.apellido}"


class Proveedor(models.Model):
    nombre_proveedor = models.CharField(max_length=255)
    tipo_servicio = models.CharField(max_length=255)
    certificado = models.FileField(upload_to="certificados/")
    doc_representacion = models.FileField(upload_to="representaciones/")
    correo = models.EmailField(unique=True)
    password = models.CharField(max_length=255)

    def __str__(self):
        return self.nombre_proveedor


class AdminExtra(models.Model):
    correo = models.EmailField(unique=True)
    codigo_otorgado = models.CharField(max_length=50)
    password = models.CharField(max_length=255)

    def __str__(self):
        return self.correo


class Reserva(models.Model):
    nombre = models.CharField(max_length=100)
    cedula = models.CharField(max_length=20)
    correo = models.EmailField()
    personas = models.IntegerField()
    fecha_inicio = models.DateField()
    fecha_final = models.DateField()
    hospedaje = models.CharField(max_length=50)
    habitaciones = models.IntegerField()
    destino = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.nombre} - {self.destino}"