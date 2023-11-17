import io
from email.message import EmailMessage
import smtplib
from dotenv import load_dotenv
import os 

def envio_resultado(titulo, mensagem, lista_de_imagens, para):
    load_dotenv()
    de = os.getenv('AUTH_EMAIL')
    senha_de = os.getenv('AUTH_PASS')
    try:
        server_ssl = smtplib.SMTP_SSL("smtp.gmail.com", 465)
        server_ssl.login(de, senha_de)  
        msg = EmailMessage()
        msg.set_content(mensagem)
        msg['Subject'] = titulo

        for i in lista_de_imagens:
            formato = "png"
            f = io.BytesIO()
            i.savefig(f, format=formato)
            f.seek(0)
            img_data = f.read()
            msg.add_attachment(img_data, maintype='image', subtype=formato)
            server_ssl.sendmail(de, para, msg.as_string())

    except Exception as e:
        # Print any error messages to stdout
        print(e)
    finally:
        server_ssl.quit() 