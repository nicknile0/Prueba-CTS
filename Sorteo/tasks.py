from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
import time

@shared_task
def enviar_correo_verificacion(email, token):
    asunto = "Verifica tu cuenta - Sorteo San Valentín"
    mensaje = f"""
    ¡Gracias por inscribirte en el Sorteo San Valentín! 💘

    Para completar tu registro, verifica tu cuenta haciendo clic en el siguiente enlace:

    http://localhost:8080/verificar?token={token}

    Si no te inscribiste, puedes ignorar este correo.
    """
    send_mail(asunto, mensaje, settings.EMAIL_HOST_USER, [email], fail_silently = False)


@shared_task
def enviar_correo_ganador(email, nombre):
    asunto = "¡Felicidades, eres el ganador del Sorteo San Valentín!"
    mensaje = f"""
    Hola {nombre},

    ¡Felicidades! Has sido seleccionado como ganador del Sorteo San Valentín 🎉

    Has ganado una estadía de 2 noches con todo pagado para ti y tu pareja en nuestro hotel.
    Pronto nos pondremos en contacto contigo para coordinar los detalles.

    ¡Gracias por participar!
    """
    send_mail(asunto, mensaje, settings.EMAIL_HOST_USER, [email], fail_silently = False)