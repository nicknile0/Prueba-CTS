import random
import uuid
from datetime import timedelta
from django.contrib.auth.hashers import make_password
from django.utils import timezone
from django.shortcuts import render
from rest_framework import generics, status, permissions, filters
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from .models import Participante, Ganador, TokenVerificacion
from .serializers import ParticipanteSerializer, LoginAdminSerializer, ListaParticipantesSerializer 
from .tasks import enviar_correo_verificacion, enviar_correo_ganador


# Create your views here.

class RegistroParticipanteView(generics.CreateAPIView):
    queryset = Participante.objects.all()
    serializer_class = ParticipanteSerializer

    def perform_create(self, serializer):
        participante = serializer.save()

        # crear token de verificación
        token_obj = TokenVerificacion.objects.create(
            participante = participante,
            token = uuid.uuid4(),
            expiracion = timezone.now() + timedelta(hours = 24)
        )
        # Llamar a tarea asíncrona
        enviar_correo_verificacion.delay(participante.email, str(token_obj.token))

class LoginAdminView(generics.GenericAPIView):
    serializer_class = LoginAdminSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data = request.data)
        serializer.is_valid(raise_exception = True)
        user = serializer.validated_data['user']

        token, created = Token.objects.get_or_create(user = user)

        return Response({
            "mensaje": f"Bienvenido, {user.nombre}",
            "email": user.email,
            "nombre": getattr(user, 'nombre', ''),
            "token": token.key
        })
    
class ListaParticipantesView(generics.ListAPIView):
    queryset = Participante.objects.all()
    serializer_class = ListaParticipantesSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter]
    search_fields = ['nombre', 'email']

class SorteoGanadorView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated] #Sólo admin

    def post(self, request):
        participantes = Participante.objects.filter(verificado = True).exclude(ganador__isnull = False)
        if not participantes.exists():
            return Response({"mensaje": "No hay participantes válidos para el sorteo."})
        
        ganador = random.choice(participantes)

        Ganador.objects.create(participante = ganador)

        enviar_correo_ganador.delay(ganador.email, ganador.nombre)

        return Response({
            "mensaje": "Ganador seleccionado",
            "nombre": ganador.nombre,
            "email": ganador.email
        })
    
class VerificarCuentaView(APIView):
    def post(self, request):
        token = request.data.get("token")
        password = request.data.get("password")

        try:
            token_obj = TokenVerificacion.objects.get(token = token)
        except TokenVerificacion.DoesNotExist:
            return Response({"detail": "Token inválido."}, status = status.HTTP_400_BAD_REQUEST)
        
        if token_obj.expiracion < timezone.now():
            return Response({"detail": "Token expirado."}, status = status.HTTP_400_BAD_REQUEST)
        
        participante = token_obj.participante
        participante.set_password(password)
        participante.verificado = True
        participante.save()

        token_obj.delete()

        return Response({"detail": "Cuenta verificada correctamente."})