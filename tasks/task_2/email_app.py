import logging
import mimetypes
import os
import smtplib

from email import encoders
from email.mime.audio import MIMEAudio
from email.mime.base import MIMEBase
from email.mime.image import MIMEImage
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header

from PyQt5 import uic
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from PyQt5.QtWidgets import QMainWindow, QMessageBox, QFileDialog

from tasks.logger import logger
from tasks.task_2.config import config
from tasks.utils import validate_email


class EmailSenderApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = uic.loadUi('files/email_form.ui', self)
        self.ui.button_send_2.clicked.connect(self.open_file_dialog) # Подключение кнопки для добавления вложений
        self.ui.button_send.clicked.connect(self.send_mail)

        # Создаем модель данных для QListView
        self.model = QStandardItemModel()
        self.ui.listView.setModel(self.model)  # Подключаем модель к QListView

        # Настройки SMTP для каждого сервиса
        self.smtp_servers = {
            # криво привязано
            0: ("smtp.yandex.ru", 465),
            1: ("smtp.gmail.com", 587),
            2: ("smtp.mail.ru", 465),
        }

        # Список для хранения путей к файлам
        self.attachments = []

    def send_mail(self):
        logger.debug("get signal")
        try:
            addr_to = self.ui.address_name_text_field.text()
            msg_subj = self.ui.theme_mail_text_field.text()
            msg_text = self.ui.text_mail_text_field.toPlainText()
            address_sender_field = self.ui.address_sender_field.text()
            password_sender_field = self.ui.password_sender_field.text()
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
            # Выбор SMTP сервера
            index = self.ui.comboBox.currentIndex()
            print("index: ", index)
            smtp_server, smtp_port = self.smtp_servers[index]

            self._send_email(addr_to, msg_subj, msg_text,
                             smtp_server=smtp_server,
                             smtp_port=smtp_port,
                             login_from=address_sender_field,
                             pass_from=password_sender_field)
            QMessageBox.information(self, "Успех", "Письмо отправлено!")
        except Exception as e:
            logger.exception(e)
            QMessageBox.critical(self, "Ошибка", f"Ошибка отправки.")  #: {e}

    def _send_email(self, addr_to, msg_subj, msg_text, smtp_server, smtp_port, login_from, pass_from):
        addr_from = login_from
        password = pass_from

        msg = MIMEMultipart()
        msg['From'] = addr_from
        msg['To'] = addr_to
        msg['Subject'] = Header(msg_subj, 'utf-8')
        msg.attach(MIMEText(msg_text, 'plain', 'utf-8'))

        # Добавление вложений
        if self.attachments:
            self.process_attachments(msg, self.attachments)

        # Отправка письма
        if smtp_port == 587:
            smtp_server = smtplib.SMTP(smtp_server, smtp_port)
            smtp_server.starttls()
        else:
            smtp_server = smtplib.SMTP_SSL(smtp_server, smtp_port)

        smtp_server.login(addr_from, password)
        smtp_server.sendmail(addr_from, [addr_to], msg.as_string())
        smtp_server.quit()

    def open_file_dialog(self):
        logger.debug("get signal from second_button")
        print("open_file_dialog")
        options = QFileDialog.Options()
        try:
            files, _ = QFileDialog.getOpenFileNames(self,
                                                    "Выберите файлы",
                                                    directory="files/mail_files/",
                                                    filter="All Files (*)",  # ;;Text Files (*.txt)
                                                    options=options)

            if files:
                self.attachments.extend(files)
                for file in files:
                    item = QStandardItem(os.path.basename(file))  # Создаем элемент
                    self.model.appendRow(item)  # Добавляем элемент в модель
                #self.ui.listView.addItems([os.path.basename(f) for f in files])
        except Exception as e:
            logger.exception(e)

    def process_attachments(self, msg, files):
        for file in files:
            if os.path.isfile(file):
                self.attach_file(msg, file)

    def attach_file(self, msg, filepath):
        filename = os.path.basename(filepath)
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

    # def open_file(self):
    #     filename = QFileDialog.getOpenFileName(
    #         parent=win,
    #         caption=u'Открыть файл',
    #         directory=PATH,
    #         filter='AllFiles (*)'
    #     )
    #     if filename:
    #         win.path = filename
    #         win.ui.label_4.setText(filename)
