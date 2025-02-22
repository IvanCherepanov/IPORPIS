import sys

from PyQt5.QtWidgets import QApplication

from tasks.task_5.calc_app import CalculatorApp


def main():
    app = QApplication(sys.argv)

    window = CalculatorApp()
    window.setFixedSize(350, 150)
    window.setWindowTitle('CalcApp')
    window.show()

    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
