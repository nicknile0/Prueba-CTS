import random
from django.utils import timezone
from django.shortcuts import render
from rest_framework import generics, status, permissions, filters
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Participante, Ganador, TokenVerificacion
from .serializers import ParticipanteSerializer, LoginAdminSerializer, ListaParticipantesSerializer 
from .tasks import enviar_correo_prueba, notificar_ganador


# Create your views here.

class RegistroParticipanteView(generics.CreateAPIView):
    queryset = Participante.objects.all()
    serializer_class = ParticipanteSerializer

    def perform_create(self, serializer):
        participante = serializer.save()
        # Llamar a tarea asíncrona
        enviar_correo_prueba.delay(participante.email)

class LoginAdminView(generics.GenericAPIView):
    serializer_class = LoginAdminSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data = request.data)
        serializer.is_valid(raise_exception = True)
        user = serializer.validated_data['user']
        return Responde({
            "mensaje": f"Bienvenido, {user.nombre}",
            "email": user.email,
            "nombre": getattr(user, 'nombre', '')
        })
    
class ListaParticipantesView(generics.ListAPIView):
    queryset = Participante.objects.all()
    serializer_class = ListaParticipantesSerializer
    permission_classes = [permissions.IsAdminUser]
    filter_backends = [filters.SearchFilter]
    search_fields = ['nombre', 'email']

class SorteoGanadorView(APIView):
    permission_classes = [permissions.IsAdminUser] #Sólo admin

    def post(self, request):
        participantes = Participante.objects.filter(verificado = True).exclude(ganador__isnull = False)
        if not participantes.exists():
            return Response({"mensaje": "No hay participantes válidos para el sorteo."})
        
        ganador = random.choice(participantes)

        Ganador.objects.create(participante = ganador)

        notificar_ganador.delay(ganador.email, ganador.nombre)

        return Response({
            "mensaje": "Ganador seleccionado",
            "nombre": ganador.nombre,
            "email": ganador.email
        })
    
class VerificarCuentaView(APIView):
    def posrt(self, request):
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