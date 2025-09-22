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
