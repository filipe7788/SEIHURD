import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import io
import os
import matplotlib.pyplot as plt
from PIL import Image
import random
import string
from dotenv import load_dotenv


def random_filename():
    # Gerar um nome de arquivo aleatório
    return ''.join(random.choices(string.ascii_letters + string.digits, k=8))


def save_images_as_one_file(lista_de_imagens):
    randomname = random_filename()
    images = [imagem.savefig(fname=randomname, format='png', bbox_inches='tight', pad_inches=0.1, format='png') for imagem in lista_de_imagens]

    # Combine as imagens em um único arquivo
    img_buffer = io.BytesIO()
    images[0].save(img_buffer, format='PNG', save_all=True, append_images=images[1:])
    
    return img_buffer.getvalue()


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
        anexo.set_payload(save_images_as_one_file(lista_de_imagens))

        # Adicionar o anexo ao corpo do e-mail
        encoders.encode_base64(anexo)
        
        msg.attach(anexo)

        # Enviar o e-mail usando smtplib diretamente
        server_ssl.sendmail(de, para, msg.as_string())

    except Exception as e:
        # Imprimir mensagens de erro
        print(e)
    finally:
        server_ssl.quit()
