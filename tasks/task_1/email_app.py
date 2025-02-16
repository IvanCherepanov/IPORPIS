import logging

from PyQt5 import uic
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header

from PyQt5.QtWidgets import QMainWindow, QMessageBox

from tasks.logger import logger
from tasks.task_1.config import config
from tasks.utils import validate_email


class EmailSenderApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = uic.loadUi('files/email_form.ui', self)
        self.ui.button_send.clicked.connect(self.send_mail)
        self.smtp_server = "smtp.yandex.ru"
        self.smtp_port = 465
        self.addr_from = config.yandex_smpt_login
        self.password = config.yandex_smpt_password

    def send_mail(self):
        logger.debug("get signal")
        try:
            addr_to = self.ui.address_name_text_field.text()
            msg_subj = self.ui.theme_mail_text_field.text()
            msg_text = self.ui.text_mail_text_field.toPlainText()
        except Exception as e:
            logger.exception(e)
            QMessageBox.information(self, "Ошибка", "Переданные данные не удалось преобразовать!")
            return

        is_email_correct = validate_email(email=addr_to)
        if not is_email_correct:
            QMessageBox.information(self, "Ошибка", "Email не соответствует формату!")
            return

        logger.debug("start send mes")
        try:
            self._send_email_yandex(addr_to, msg_subj, msg_text)
            QMessageBox.information(self, "Успех", "Письмо отправлено!")
        except Exception as e:
            logger.exception(e)
            QMessageBox.critical(self, "Ошибка", f"Ошибка отправки.")  #: {e}

    def _send_email_yandex(self, addr_to, msg_subj, msg_text):
        addr_from = self.addr_from
        password = self.password

        msg = MIMEMultipart()
        msg['From'] = addr_from
        msg['To'] = addr_to
        msg['Subject'] = Header(msg_subj, 'utf-8')
        msg.attach(MIMEText(msg_text, 'plain', 'utf-8'))

        server = smtplib.SMTP_SSL(self.smtp_server, self.smtp_port)
        server.login(addr_from, password)
        server.sendmail(addr_from, [addr_to], msg.as_string())
        server.quit()
