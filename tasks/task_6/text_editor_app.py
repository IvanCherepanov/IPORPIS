from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QFileDialog, QMessageBox
from PyQt5.QtGui import QFont

from tasks.logger import logger


class TextEditorApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = uic.loadUi('files/text_editor_updated.ui', self)

        # Подключаем кнопки
        self.ui.actionopen.triggered.connect(self.open_file)  # Подключение кнопки для добавления вложений
        self.ui.actionsave.triggered.connect(self.save_file)

        # Подключаем элементы стиля текста
        self.actionitalic.triggered.connect(self.set_bold)
        self.actionbold.triggered.connect(self.set_italic)
        self.actionunderline.triggered.connect(self.set_underline)

    def open_file(self):
        try:
            self.setWindowTitle("Текстовый редактор")  # Сброс названия при открытии нового файла
            file_name, _ = QFileDialog.getOpenFileName(self, "Открыть файл", "", "Текстовые файлы (*.txt);;Все файлы (*.*)")
            if file_name:
                self.setWindowTitle(f"Текстовый редактор - {file_name.split('/')[-1]}")
                with open(file_name, 'r', encoding='utf-8') as file:
                    self.textEdit.setHtml(file.read())  # .replace('\n',' < br > ')

        except Exception as e:
            logger.exception(e)
            QMessageBox.critical(self, "Ошибка", f"Ошибка при открытии: {str(e)}")

    def save_file(self):
        file_name, _ = QFileDialog.getSaveFileName(self, "Сохранить файл", "",
                                                   "Текстовые файлы (*.txt);;Все файлы (*.*)")
        if file_name:
            with open(file_name, 'w', encoding='utf-8') as file:
                file.write(self.textEdit.toHtml())

    def set_bold(self):
        fmt = self.textEdit.textCursor().charFormat()
        fmt.setFontWeight(
            QFont.Weight.Bold if fmt.fontWeight() != QFont.Weight.Bold else QFont.Weight.Normal)
        self.textEdit.textCursor().mergeCharFormat(fmt)

    def set_italic(self):
        fmt = self.textEdit.textCursor().charFormat()
        fmt.setFontItalic(not fmt.fontItalic())
        self.textEdit.textCursor().mergeCharFormat(fmt)

    def set_underline(self):
        fmt = self.textEdit.textCursor().charFormat()
        fmt.setFontUnderline(not fmt.fontUnderline())
        self.textEdit.textCursor().mergeCharFormat(fmt)
