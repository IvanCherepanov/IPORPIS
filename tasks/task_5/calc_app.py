from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QMessageBox

from tasks.logger import logger
from tasks.task_5.algo import calculate


class CalculatorApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = uic.loadUi('files/calculator_app.ui', self)
        self.ui.button_count.clicked.connect(self.calculate_expression)  # Подключение кнопки для добавления вложений

    def calculate_expression(self):
        logger.debug("get signal")

        try:
            expression = self.ui.expression_input_field.text()
        except Exception as e:
            logger.exception(e)
            QMessageBox.information(self, "Ошибка", "Переданные данные не удалось преобразовать!")
            return

        try:
            result = self._do(request=expression)
            self.ui.output_label.setText(str(result))

        except Exception as e:
            logger.exception(e)
            QMessageBox.critical(self, "Ошибка", f"Ошибка при рассчете выражения: {str(e)}")

    def _do(self, request: str) -> int:
        return calculate(expression=request)
