import uuid
from django.utils import timezone
from datetime import timedelta
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, AbstractUser, BaseUserManager


# Create your models here.

class ParticipanteManager(BaseUserManager):
    def create_user(self, email, nombre, telefono, password = None):
        if not email:
            raise ValueError('El participante debe tener un email válido')
        user = self.model(
            email = self.normalize_email(email),
            nombre = nombre,
            telefono = telefono
        )
        user.set_password(password)
        user.save(using = self._db)
        return user
    
    def create_superuser(self, email, nombre, telefono, password):
        user = self.create_user(email, nombre, telefono, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using = self._db)
        return user
        
class Participante(AbstractBaseUser):
    email = models.EmailField(unique = True)
    nombre = models.CharField(max_length = 100)
    telefono = models.CharField(max_length = 15)
    verificado = models.BooleanField(default = False)
    activo = models.BooleanField(default = True)
    es_staff = models.BooleanField(default = False)

    objects = ParticipanteManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['nombre', 'telefono']

    def __str__(self):
        return self.email
    
def obtener_expiracion():
    return timezone.now() + timedelta(hours = 24)

class TokenVerificacion(models.Model):
    participante = models.ForeignKey(Participante, on_delete = models.CASCADE)
    token = models.UUIDField(default = uuid.uuid4, unique = True, editable = False)
    creado = models.DateTimeField(auto_now_add = True)
    expiracion = models.DateTimeField(default = obtener_expiracion)

    def __str__(self):
        return f"{self.participante.email} - {self.token}"
    
class Ganador(models.Model):
    participante = models.OneToOneField(Participante, on_delete = models.CASCADE)
    fecha_sorteo = models.DateTimeField(auto_now_add = True)

    def __str__(self):
        return f"{self.participante.nombre} - {self.participante.email}"