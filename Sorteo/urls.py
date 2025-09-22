from django.urls import path
from .views import RegistroParticipanteView, LoginAdminView, ListaParticipantesView, SorteoGanadorView


urlpatterns = [
    path('registro/', RegistroParticipanteView.as_view(), name = 'registro-participante'),
    path('admin/login/', LoginAdminView.as_view(), name = 'login-admin'),
    path('admin/participantes/', ListaParticipantesView.as_view(), name = 'lista-participantes'),
    path('admin/sorteo/', SorteoGanadorView.as_view(), name = 'sorteo-ganador'),
]