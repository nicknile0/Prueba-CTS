import random
from django.shortcuts import render
from rest_framework import generics, status, permissions, filters
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Participante, Ganador
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