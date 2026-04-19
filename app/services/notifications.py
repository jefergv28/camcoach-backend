# notifications.py
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from twilio.rest import Client

# Configuración Twilio
TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
TWILIO_WHATSAPP_NUMBER = os.getenv("TWILIO_WHATSAPP_NUMBER")
TWILIO_SMS_NUMBER = os.getenv("TWILIO_SMS_NUMBER")  # Tu número Twilio para SMS

# Configuración Email
EMAIL_USER = os.getenv("EMAIL_USER")
EMAIL_PASS = os.getenv("EMAIL_PASS")
EMAIL_SENDER = os.getenv("EMAIL_SENDER", EMAIL_USER)


def enviar_whatsapp(telefono: str, evento: dict):
    """
    Envía un mensaje de WhatsApp con los detalles del evento.
    """
    mensaje = (
        f"Hola {evento.get('cliente')},\n\n"
        f"Recordatorio de tu cita:\n"
        f"Asunto: {evento.get('titulo')}\n"
        f"Fecha: {evento.get('fecha')}\n"
        f"Hora: {evento.get('hora') or 'Por confirmar'}\n"
        f"Descripción: {evento.get('descripcion') or 'N/A'}\n\n"
        f"¡Nos vemos pronto! CamCoach"
    )
    try:
        client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
        client.messages.create(
            from_=TWILIO_WHATSAPP_NUMBER,
            body=mensaje,
            to=f"whatsapp:{telefono}"
        )
        print(f"WhatsApp enviado a {telefono}")
    except Exception as e:
        print(f"Error WhatsApp: {e}")


def enviar_sms(telefono: str, evento: dict):
    """
    Envía un SMS con los detalles del evento usando Twilio.
    """
    mensaje = (
        f"Hola {evento.get('cliente')}, recordatorio de tu cita:\n"
        f"{evento.get('titulo')} el {evento.get('fecha')} "
        f"a las {evento.get('hora') or 'Por confirmar'}.\n"
        f"CamCoach"
    )
    try:
        client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
        client.messages.create(
            from_=TWILIO_SMS_NUMBER,
            body=mensaje,
            to=telefono
        )
        print(f"SMS enviado a {telefono}")
    except Exception as e:
        print(f"Error SMS: {e}")


def enviar_correo(destinatario: str, asunto: str, evento: dict):
    """
    Envía un correo profesional en HTML para un evento.
    `evento` debe ser un dict con claves: titulo, fecha, hora, descripcion, cliente.
    """
    # Crear el correo como multipart para soporte HTML
    msg = MIMEMultipart("alternative")
    msg["Subject"] = asunto
    msg["From"] = EMAIL_SENDER
    msg["To"] = destinatario

    # Contenido en texto plano
    texto = f"""
Hola {evento.get('cliente')},

Te recordamos tu cita:

Asunto: {evento.get('titulo')}
Fecha: {evento.get('fecha')}
Hora: {evento.get('hora') or 'Por confirmar'}
Descripción: {evento.get('descripcion') or 'N/A'}

¡Nos vemos pronto!
"""

    # Contenido en HTML
    html = f"""
<html>
  <body style="font-family: Arial, sans-serif; background-color:#f4f4f4; padding:20px;">
    <div style="max-width:600px; margin:auto; background-color:#ffffff; border-radius:8px; padding:20px; border:1px solid #ddd;">
      <h2 style="color:#1a73e8;">Recordatorio de Cita</h2>
      <p>Hola <strong>{evento.get('cliente')}</strong>,</p>
      <p>Te recordamos tu próxima cita:</p>
      <table style="width:100%; border-collapse: collapse;">
        <tr>
          <td style="padding:8px; border:1px solid #ddd;"><strong>Asunto:</strong></td>
          <td style="padding:8px; border:1px solid #ddd;">{evento.get('titulo')}</td>
        </tr>
        <tr>
          <td style="padding:8px; border:1px solid #ddd;"><strong>Fecha:</strong></td>
          <td style="padding:8px; border:1px solid #ddd;">{evento.get('fecha')}</td>
        </tr>
        <tr>
          <td style="padding:8px; border:1px solid #ddd;"><strong>Hora:</strong></td>
          <td style="padding:8px; border:1px solid #ddd;">{evento.get('hora') or 'Por confirmar'}</td>
        </tr>
        <tr>
          <td style="padding:8px; border:1px solid #ddd;"><strong>Descripción:</strong></td>
          <td style="padding:8px; border:1px solid #ddd;">{evento.get('descripcion') or 'N/A'}</td>
        </tr>
      </table>
      <p style="margin-top:20px;">¡Nos vemos pronto!<br>El equipo de <strong>CamCoach</strong></p>
    </div>
  </body>
</html>
"""

    # Adjuntar ambas versiones
    msg.attach(MIMEText(texto, "plain"))
    msg.attach(MIMEText(html, "html"))

    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(EMAIL_USER, EMAIL_PASS)
            server.send_message(msg)
        print(f"Correo enviado a {destinatario}")
    except Exception as e:
        print(f"Error Email: {e}")