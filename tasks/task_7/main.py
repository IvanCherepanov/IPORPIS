import sys

from PyQt5.QtWidgets import QApplication

from tasks.task_7.database_app import DatabaseApp


def main():
    app = QApplication(sys.argv)

    window = DatabaseApp()
    window.setFixedSize(800, 700)
    window.setWindowTitle('DatabaseAppApp')
    window.show()

    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
