import os
from email import encoders
from email.mime.audio import MIMEAudio
from email.mime.base import MIMEBase
from email.mime.image import MIMEImage
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header
import smtplib
import mimetypes
from pathlib import Path

from tasks.logger import logger

smtp_servers = {
    0: ("smtp.yandex.ru", 465),
    1: ("smtp.gmail.com", 587),
    2: ("smtp.mail.ru", 465),
}
attachments_folder = os.path.join(Path(__file__).parent.parent,"files\mail_files")


def send_email(addr_to, msg_subj, msg_text, smtp_server, smtp_port, login_from, pass_from, attachments):
    msg = MIMEMultipart()
    msg['From'] = login_from
    msg['To'] = addr_to
    msg['Subject'] = Header(msg_subj, 'utf-8')
    msg.attach(MIMEText(msg_text, 'plain', 'utf-8'))

    for file in attachments:
        filepath = file  # Изначально используем путь из CSV

        # Если файл не существует, добавляем путь до папки с вложениями
        if not os.path.isfile(filepath):
            filepath = os.path.join(attachments_folder, file)
        if os.path.isfile(filepath):
            logger.debug(f"file: {file} with {filepath} exist")
            attach_file(msg, filepath)
        else:
            logger.debug(f"file:{file} with {filepath} not exist")

    if smtp_port == 587:
        smtp = smtplib.SMTP(smtp_server, smtp_port)
        smtp.starttls()
    else:
        smtp = smtplib.SMTP_SSL(smtp_server, smtp_port)

    smtp.login(login_from, pass_from)
    smtp.sendmail(login_from, [addr_to], msg.as_string())
    smtp.quit()


def attach_file(msg, filepath):
    filename = filepath.split('/')[-1]
    ctype, encoding = mimetypes.guess_type(filepath)

    if ctype is None or encoding is not None:
        ctype = 'application/octet-stream'
    maintype, subtype = ctype.split('/', 1)

    with open(filepath, 'rb') as fp:
        if maintype == 'text':
            file = MIMEText(fp.read().decode('utf-8'), _subtype=subtype)
        elif maintype == 'image':
            file = MIMEImage(fp.read(), _subtype=subtype)
        elif maintype == 'audio':
            file = MIMEAudio(fp.read(), _subtype=subtype)
        else:
            file = MIMEBase(maintype, subtype)
            file.set_payload(fp.read())
            encoders.encode_base64(file)

        file.add_header('Content-Disposition', 'attachment', filename=filename)
        msg.attach(file)
