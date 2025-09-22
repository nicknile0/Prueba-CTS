from celery import shared_task
import time

@shared_task
def enviar_correo_prueba(email):
    time.sleep(3)
    return f"Correo enviado a {email}"

@shared_task
def notificar_ganador(email, nombre):
    return f"Ganador {nombre} notificado al correo {email}"