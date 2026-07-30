import os 
import smtplib
import requests
from dotenv import load_dotenv
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

load_dotenv()

def obter_datos_clima(ciudad, api_key):
    url = f"https://api.openweathermap.org/data/2.5/weather?q={ciudad}&appid={api_key}&lang=es&units=metric"
    try:
        response = requests.get(url)
        response.raise_for_status()
        # Corregido: extraemos directamente el JSON estructurado
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

if __name__ == "__main__":
    ciudad = os.getenv('CIUDAD')
    api_key = os.getenv('API_KEY_OPENWEATHERMAP')
    destinatario = os.getenv('CORREO_DESTINATARIO')
    
    print("\n--- Ejecutando reporte del clima instantáneo ---")
    print(f"Obteniendo datos del clima para: {ciudad}...")
    
    datos_clima = obter_datos_clima(ciudad, api_key)
    if datos_clima:
        # Se corrigió la lectura del diccionario ['weather'][0] para evitar fallos
        descripcion = datos_clima['weather'][0]['description']
        temp = datos_clima['main']['temp']
        
        print(f"Clima en {ciudad}: {descripcion}, Temperatura: {temp}°C")
        
        contenido_email = f"Clima en {ciudad}: {descripcion}, Temperatura: {temp}°C"
        asunto = f"Reporte del clima - {ciudad}"
        
        print("Enviando correo electrónico...")
        enviar_email(destinatario, asunto, contenido_email)