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

    # Informações de disparo do email:
    EMAIL_QUE_IRA_DISPARAR = email_de_disparo
    SENHA_DO_EMAIL_DE_DISPARO = senha_do_email_de_disparo
    MENSAGEM = "Estou passando para avisar, que sua fila foi aceita."

    # criando instancia do objeto de mensagem
    msg = MIMEMultipart()

    msg['From'] = EMAIL_QUE_IRA_DISPARAR
    msg['To'] = email_destinatario
    msg['Subject'] = "LOL - Partida Encontrada"

    # adicionando mensagem ao corpo
    msg.attach(MIMEText(MENSAGEM, 'plain'))

    contexto = ssl.create_default_context()
    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as servidor:
            servidor.ehlo()  # Pode ser omitido
            servidor.starttls(context=contexto)
            servidor.ehlo()  # Pode ser omitido
            servidor.login(EMAIL_QUE_IRA_DISPARAR, SENHA_DO_EMAIL_DE_DISPARO)
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


def cadastrar_email_que_ira_enviar_notificao(email_de_disparo, senha_do_email_de_disparo, email_destinatario):
    nao_possui_informacao_de_envio = len(
        email_de_disparo) == 0 and len(senha_do_email_de_disparo) == 0
    if(nao_possui_informacao_de_envio):
        return

    enviar_email_de_notificacao(
        email_de_disparo, senha_do_email_de_disparo, email_destinatario)


def verificar_se_possui_dados_de_disparo_e_de_envio():
    email_de_disparo = input(
        'Seu email que irá disparar a notificação(opcional): ').strip()

    informou_email_de_disparo = len(email_de_disparo) != 0
    if(informou_email_de_disparo):
        senha_do_email_de_disparo = input(
            'Senha do seu email que irá disparar a notificação(opcional): ').strip()
        email_destinatario = input(
            'Seu email que irá receber a notificação(opcional): ').strip()
        return email_de_disparo, senha_do_email_de_disparo, email_destinatario


def main():
    email_de_disparo, senha_do_email_de_disparo, email_destinatario = verificar_se_possui_dados_de_disparo_e_de_envio()

    while True:
        encontrou_o_botao_na_tela = verificar_tela()
        if(encontrou_o_botao_na_tela):
            cadastrar_email_que_ira_enviar_notificao(
                email_de_disparo, senha_do_email_de_disparo, email_destinatario)
            sleep(6)


main()
