from rest_framework import serializers
from .models import Participante
from django.contrib.auth import authenticate


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
        user = authenticate(username = data['email'], password = data['password'])
        if not user or not user.is_staff:
            raise serializers.ValidationError("credenciales inválidas o usuario no administrador.")
        data['user'] = user
        return data
    
class ListaParticipantesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Participante
        fields = ['id', 'nombre', 'email', 'telefono', 'verificado']