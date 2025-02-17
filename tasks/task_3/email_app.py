import csv
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
from pathlib import Path

from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QMessageBox, QFileDialog

from tasks.logger import logger
from tasks.utils import validate_email


class EmailSenderApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = uic.loadUi('files/email_form.ui', self)
        self.ui.button_send_2.clicked.connect(self.open_csv_file)  # Подключение кнопки для добавления вложений
        self.ui.button_send.clicked.connect(self.send_mail)

        self.smtp_servers = {
            # криво привязано
            0: ("smtp.yandex.ru", 465),
            1: ("smtp.gmail.com", 587),
            2: ("smtp.mail.ru", 465),
        }

        self.attachments = []  # Список для хранения путей к файлам
        self.csv_file_path = None  # Путь к CSV-файлу
        self.attachments_folder = os.path.join(Path(__file__).parent,"files\mail_files")  # Папка с вложениями

    def send_mail(self):
        logger.debug("get signal")
        if not self.csv_file_path:
            QMessageBox.warning(self, "Ошибка", "CSV файл не выбран!")
            return

        try:
            msg_subj = self.ui.theme_mail_text_field.text()
            msg_text = self.ui.text_mail_text_field.toPlainText()
            address_sender_field = self.ui.address_sender_field.text()
            password_sender_field = self.ui.password_sender_field.text()
        except Exception as e:
            logger.exception(e)
            QMessageBox.information(self, "Ошибка", "Переданные данные не удалось преобразовать!")
            return

        # Выбор SMTP сервера
        index = self.ui.comboBox.currentIndex()
        print("index: ", index)
        smtp_server, smtp_port = self.smtp_servers[index]

        try:
            with open(self.csv_file_path, "r", encoding="utf-8") as csv_file:
                reader = csv.reader(csv_file)
                for row in reader:
                    if not row:
                        continue

                    # Разделение строки на адресата и файлы
                    parts = row[0].split(";")
                    addr_to = parts[0].strip()
                    files = [f.strip() for f in parts[1:] if f.strip()]
                    logger.debug(f"for email: {addr_to} files: {files}; row: {row}")

                    # Проверка email адреса
                    if not validate_email(addr_to):
                        self.log(f"Ошибка: Некорректный email адрес {addr_to}")
                        continue

                    # Отправка письма
                    try:
                        self._send_email(addr_to, msg_subj, msg_text,
                                        smtp_server=smtp_server,
                                        smtp_port=smtp_port,
                                        login_from=address_sender_field,
                                        pass_from=password_sender_field,
                                        attachments=files)
                        self.log(f"Email {addr_to}; theme: {msg_subj}; message: {msg_text}")
                    except Exception as e:
                        logger.exception(e)
                        self.log(f"Ошибка отправки письма {addr_to}: {str(e)}")
            QMessageBox.information(self, "Успех", "Файл обработан! Смотрите лог.файл для проверки!")

        except Exception as e:
            logger.exception(e)
            QMessageBox.critical(self, "Ошибка", f"Ошибка при чтении CSV файла: {str(e)}")

    def _send_email(self, addr_to, msg_subj, msg_text, smtp_server, smtp_port, login_from, pass_from, attachments):
        addr_from = login_from
        password = pass_from

        msg = MIMEMultipart()
        msg['From'] = addr_from
        msg['To'] = addr_to
        msg['Subject'] = Header(msg_subj, 'utf-8')
        msg.attach(MIMEText(msg_text, 'plain', 'utf-8'))

        # Добавление вложений
        if attachments:
            logger.debug("detected files: in process")
            self.process_attachments(msg, attachments)

        # Отправка письма
        if smtp_port == 587:
            smtp_server = smtplib.SMTP(smtp_server, smtp_port)
            smtp_server.starttls()
        else:
            smtp_server = smtplib.SMTP_SSL(smtp_server, smtp_port)

        smtp_server.login(addr_from, password)
        smtp_server.sendmail(addr_from, [addr_to], msg.as_string())
        smtp_server.quit()

    def open_csv_file(self):
        # todo: растащить логику открытия файла и имзменение ui, если будет время
        """Открытие CSV-файла"""
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getOpenFileName(
            self,  # Родительское окно
            "Выберите CSV файл",  # Заголовок окна
            "",  # Начальная директория
            "CSV Files (*.csv);;All Files (*)",  # Фильтры файлов
            options=options
        )

        if file_name:
            self.csv_file_path = file_name
            self.ui.label_csv_path.setText(f"Выбран файл: {os.path.basename(file_name)}")

    def process_attachments(self, msg, files):
        for file in files:
            logger.debug(f"file: {file}")
            filepath = file  # Изначально используем путь из CSV

            # Если файл не существует, добавляем путь до папки с вложениями
            if not os.path.isfile(filepath):
                filepath = os.path.join(self.attachments_folder, file)

            if os.path.isfile(filepath):
                logger.debug(f"file: {file} with {filepath} exist")
                self.attach_file(msg, filepath)
            else:
                logger.debug(f"file:{file} with {filepath} not exist")

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

    def log(self, message):
        """Логирование в файл"""
        with open("send.txt", "a", encoding="utf-8") as log_file:
            log_file.write(message + "\n")
