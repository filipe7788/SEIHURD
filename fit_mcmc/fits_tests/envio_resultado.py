import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import io
import os
import matplotlib.pyplot as plt
from dotenv import load_dotenv

def envio_resultado(titulo, mensagem, lista_de_imagens, para):
    load_dotenv()
    de = os.getenv('AUTH_EMAIL')
    senha_de = os.getenv('AUTH_PASS')

    try:
        server_ssl = smtplib.SMTP_SSL("smtp.gmail.com", 465)
        server_ssl.login(de, senha_de)

        # Construir a mensagem MIME
        msg = MIMEMultipart()
        msg['Subject'] = titulo
        msg['From'] = de
        msg['To'] = para

        # Adicionar corpo do e-mail (texto/html)
        msg.attach(MIMEText(mensagem, 'html'))

        # Criar um único anexo para todas as imagens
        anexo = MIMEBase('application', 'octet-stream')
        anexo.set_payload(io.BytesIO(b''.join([imagem.savefig(format='png', bbox_inches='tight').to_buffer() for imagem in lista_de_imagens])).read())

        # Adicionar o anexo ao corpo do e-mail
        encoders.encode_base64(anexo)
        anexo.add_header('Content-Disposition', 'attachment; filename=imagens.png')
        msg.attach(anexo)

        # Enviar o e-mail usando smtplib diretamente
        server_ssl.sendmail(de, para, msg.as_string())

    except Exception as e:
        # Imprimir mensagens de erro
        print(e)
    finally:
        server_ssl.quit()
