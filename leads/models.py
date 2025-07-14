from django.db import models

class Lead(models.Model):
    nombre = models.CharField(max_length=255, blank=True, null=True)
    apellido = models.CharField(max_length=255, blank=True, null=True)
    cargo = models.CharField(max_length=255, blank=True, null=True)
    empresa = models.CharField(max_length=255, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    telefono = models.CharField(max_length=50, blank=True, null=True)
    pais = models.CharField(max_length=100, blank=True, null=True)
    ip = models.GenericIPAddressField(blank=True, null=True)
    fecha_envio = models.DateTimeField()
    envio_id = models.IntegerField()  # ID del envío en la API fuente
    fuente = models.CharField(max_length=100, default='Hyvolution')  # para distinguir entre ferias

    class Meta:
        unique_together = ('envio_id', 'fuente')  # Evita duplicados al importar

    def __str__(self):
        return f"{self.nombre} {self.apellido} - {self.empresa}"
