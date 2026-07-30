import os 
import time
import smtplib
import requests
import schedule
from dotenv import load_dotenv
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

load_dotenv()

def obter_datos_clima(ciudad, api_key):
    url = f"https://api.openweathermap.org/data/2.5/weather?q={ciudad}&appid={api_key}&lang=es&units=metric"
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
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
            print("Email enviado correctamente.")
    except Exception as e:
        print(f"Error al enviar email: {e}")

# Encapsulamos tu lógica principal en una función ejecutable
def tarea_principal():
    ciudad = os.getenv('CIUDAD')
    api_key = os.getenv('API_KEY_OPENWEATHERMAP')
    destinatario = os.getenv('CORREO_DESTINATARIO')
    
    print("\n--- Iniciando tarea programada ---")
    print(f"Obteniendo datos del clima para: {ciudad}...")
    
    datos_clima = obter_datos_clima(ciudad, api_key)
    if datos_clima:
        descripcion = datos_clima['weather'][0]['description']
        temp = datos_clima['main']['temp']
        
        print(f"Clima en {ciudad}: {descripcion}, Temperatura: {temp}°C")
        
        contenido_email = f"Clima en {ciudad}: {descripcion}, Temperatura: {temp}°C"
        asunto = f"Reporte del clima - {ciudad}"
        
        enviar_email(destinatario, asunto, contenido_email)

if __name__ == "__main__":
    # Prepara la librería externa en la terminal antes de correrlo: pip install schedule
    print("Servicio de clima iniciado. Esperando las horas programadas...")
    print("Se enviará un correo con el clima a las 15:00 y 17:00 horas.")
    
    # Programación de tareas de forma diaria
    schedule.every().day.at("15:00").do(tarea_principal)
    schedule.every().day.at("17:00").do(tarea_principal)

    # Bucle infinito para mantener el script escuchando el reloj del sistema
    while True:
        schedule.run_pending()
        time.sleep(60) # Revisa cada minuto si corresponde ejecutar el script