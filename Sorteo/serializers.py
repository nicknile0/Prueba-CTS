from rest_framework import serializers
from .models import Participante
from django.contrib.auth.hashers import check_password


class ParticipanteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Participante
        fields = ['id', 'nombre', 'email', 'telefono', 'verificado']
        read_only_fields = ['verificado']

    def validate_email(self, value):
        if Participante.objects.filter(email = value).exists():
            raise serializers.ValidationError("Este email ya está registrado.")
        return value
    
class LoginAdminSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only = True)

    def validate(self, data):
        try:
            user = Participante.objects.get(email=data['email'])
        except Participante.DoesNotExist:
            raise serializers.ValidationError("Credenciales inválidas o usuario no administrador.")
        
        # Verificar contraseña
        if not check_password(data['password'], user.password):
            raise serializers.ValidationError("Credenciales inválidas o usuario no administrador.")

        # Verificar permisos de admin
        if not user.is_staff:  
            raise serializers.ValidationError("Credenciales inválidas o usuario no administrador.")

        data['user'] = user
        return data
    
class ListaParticipantesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Participante
        fields = ['id', 'nombre', 'email', 'telefono', 'verificado']