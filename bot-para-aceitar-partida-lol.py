import pyautogui
from time import sleep
import smtplib
import ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def clicar_para_aceitar(posicaoX, posicaoY):
    pyautogui.moveTo(posicaoX, posicaoY)
    pyautogui.click()


def enviar_email_de_notificacao(email_de_disparo, senha_do_email_de_disparo, email_destinatario):
    nao_deseja_receber_email = len(email_destinatario) == 0
    if(nao_deseja_receber_email):
        return

    mensagem = "Estou passando para avisar, que sua fila foi aceita."

    msg = MIMEMultipart()

    msg['From'] = email_de_disparo
    msg['To'] = email_destinatario
    msg['Subject'] = "LOL - Partida Encontrada"

    msg.attach(MIMEText(mensagem, 'plain'))

    contexto = ssl.create_default_context()
    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as servidor:
            servidor.ehlo()
            servidor.starttls(context=contexto)
            servidor.ehlo()
            servidor.login(email_de_disparo, senha_do_email_de_disparo)
            servidor.sendmail(msg['From'], msg['To'], msg.as_string())
    except:
        print('Não foi possível enviar email de notificaçao para "' +
              email_destinatario + '"')


def verificar_tela():
    posicao_do_botao = pyautogui.locateOnScreen('fila.png', confidence=0.7)

    encontrou_o_botao_na_tela = posicao_do_botao != None
    if(encontrou_o_botao_na_tela):
        clicar_para_aceitar(posicao_do_botao.left, posicao_do_botao.top)
        return True

    return False


def disparar_email(email_de_disparo, senha_do_email_de_disparo, email_destinatario):
    nao_possui_informacao_de_envio = len(
        email_de_disparo) == 0 and len(senha_do_email_de_disparo) == 0
    if(nao_possui_informacao_de_envio):
        return

    enviar_email_de_notificacao(
        email_de_disparo, senha_do_email_de_disparo, email_destinatario)


def nao_esta_vazio(string):
    return bool(string and not string.isspace())


def main():
    email_de_disparo = input(
        'Email que irá disparar a notificação(opcional): ').strip()

    if(nao_esta_vazio(email_de_disparo)):
        senha_do_email_de_disparo = input(
            'Senha do email que irá disparar a notificação(opcional): ').strip()
        email_destinatario = input(
            'Email que irá receber a notificação(opcional): ').strip()

    print("Estamos de olho para você... ")
    while True:
        encontrou_o_botao_na_tela = verificar_tela()
        if(encontrou_o_botao_na_tela):
            disparar_email(
                email_de_disparo, senha_do_email_de_disparo, email_destinatario)
            sleep(6)


main()
