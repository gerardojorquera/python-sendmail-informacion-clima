import requests
import smtplib
import os 
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv

load_dotenv()
def obter_datos_clima(ciudad, api_key):
    url = f"https://api.openweathermap.org/data/2.5/weather?q={ciudad}&appid={api_key}&lang=es&units=metric"
    try:
        response = requests.get(url)
        response.raise_for_status()
        datos = response.json()
        return datos
    except requests.exceptions.RequestException as e:
        print(f"Error al obtener datos del clima: {e}")
        return None
    
def enviar_email(destinatario, asunto, contenido):
    remitente = os.getenv('CORREO_REMITENTE')
    password = os.getenv('CORREO_CONTRASENA')

    msg = MIMEMultipart()
    msg['From'] = remitente
    msg['To'] = destinatario
    msg['Subject'] = asunto
    msg.attach(MIMEText(contenido, 'plain'))

    try:
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(remitente, password)
            server.send_message(msg)
            server.quit()
            print("Email enviado correctamente.")
    except Exception as e:
        print(f"Error al enviar email: {e}")

if __name__ == "__main__":
    ciudad = os.getenv('CIUDAD')
    api_key = os.getenv('API_KEY_OPENWEATHERMAP')
    print("Obteniendo datos del clima...")
    print(f"Ciudad: {ciudad}") 
    print(f"API Key: {api_key[:10]}******")
    datos_clima = obter_datos_clima(ciudad, api_key)
    if datos_clima:
        print(f"Clima en {ciudad}: {datos_clima['weather'][0]['description']}, Temperatura: {datos_clima['main']['temp']}°C")
        print("*** Datos del clima obtenidos correctamente ***")
        contenido_email = f"Clima en {ciudad}: {datos_clima['weather'][0]['description']}, Temperatura: {datos_clima['main']['temp']}°C"
        print("Contenido del email preparado.")
        destinatario = os.getenv('CORREO_DESTINATARIO')
        print(f"Destinatario del email: {destinatario}")
        asunto = f"Clima actual en {ciudad}"
        enviar_email(destinatario, asunto, contenido_email)
    else:
        print("Error al obtener datos del clima.")