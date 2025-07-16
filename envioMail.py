import smtplib  #Libreria para mandar mails 
import os     #Libreria para tener control de escritorio etc 
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv
import random


load_dotenv()

def obtener_frase (): #Esta funcion solamente toma las frases del TXT
    ruta = os.getenv("FRASES_PATH")
    if not ruta or not os.path.isfile(ruta):
        raise FileNotFoundError(f"No se encontró el archivo en la ruta: {ruta}")  #Excepcion sino encuentra el archivo

    with open(ruta, "r", encoding="utf-8") as archivo:
        frases = [linea.strip() for linea in archivo if linea.strip()]
    
    if not frases:
        raise ValueError("El archivo de frases está vacío.")
    
    print ("llego aca")
    return random.choice(frases)


def envio_mail (remitente, password, destinatario, asunto, contenido):

    mensaje = MIMEMultipart()
    mensaje ["From"] = remitente
    mensaje ["To"] = destinatario
    mensaje ["Subject"] = asunto

    mensaje.attach(MIMEText(contenido, 'plain'))

    try:
        server = smtplib.SMTP ('smtp.gmail.com', 587)
        server.starttls()
        server.login(remitente, password)
        server.sendmail(remitente, destinatario, mensaje.as_string())
        server.quit()
        print ("Correo enviado")
    except Exception as e:
        print (f"Error al correr el proceso: {e}")

if __name__ == "__main__":
    #Lee las variables del .env
    CORREO_REMITENTE= os.getenv("CORREO_REMITENTE")
    CONSTRASENA= os.getenv("CONTRASENA")
    CORREO_DESTINATARIO= os.getenv("CORREO_DESTINATARIO")

    fraseParaEnvio = obtener_frase()
    if fraseParaEnvio:
        contenido = (
             f"Hola mi amor: \n\n "
             f"Te envio la frase del dia: \n\n "      
             f"{fraseParaEnvio} \n\n "
             f"¡Que tengas buen dia, te amo!"
        )
    envio_mail(CORREO_REMITENTE,CONSTRASENA,CORREO_DESTINATARIO, f"Frase del dia", contenido)
    
