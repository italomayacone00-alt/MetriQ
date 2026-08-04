"""
Envio de e-mails via SMTP.

Se o servidor de e-mail estiver configurado (MAIL_SERVER), envia de verdade.
Se não estiver configurado (modo desenvolvimento), retorna False e loga o link
para que as rotas possam exibi-lo ao usuário na tela.
"""
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from flask import current_app, render_template


def enviar_email(destinatario, assunto, template_html, contexto=None):
    """
    Envia um e-mail HTML.
    Retorna True se enviado com sucesso.
    Retorna False se não houver servidor SMTP configurado (modo dev).
    """
    server = current_app.config.get('MAIL_SERVER')
    if not server:
        current_app.logger.warning(
            f"[E-MAIL NÃO CONFIGURADO] Para: {destinatario} | Assunto: {assunto}"
        )
        return False

    remetente = current_app.config.get('MAIL_DEFAULT_SENDER', 'nao-responda@metriq.com.br')
    corpo = render_template(template_html, **(contexto or {})) if template_html else ''

    msg = MIMEMultipart('alternative')
    msg['Subject'] = assunto
    msg['From'] = remetente
    msg['To'] = destinatario
    msg.attach(MIMEText(corpo, 'html', 'utf-8'))

    try:
        port = current_app.config.get('MAIL_PORT', 587)
        use_ssl = current_app.config.get('MAIL_USE_SSL', False)
        use_tls = current_app.config.get('MAIL_USE_TLS', True)
        username = current_app.config.get('MAIL_USERNAME')
        password = current_app.config.get('MAIL_PASSWORD')

        if use_ssl:
            smtp = smtplib.SMTP_SSL(server, port)
        else:
            smtp = smtplib.SMTP(server, port)
            smtp.ehlo()
            if use_tls:
                smtp.starttls()
                smtp.ehlo()

        if username and password:
            smtp.login(username, password)

        smtp.sendmail(remetente, [destinatario], msg.as_string())
        smtp.quit()
        return True

    except Exception as e:
        current_app.logger.error(f"Erro ao enviar e-mail: {e}")
        return False

