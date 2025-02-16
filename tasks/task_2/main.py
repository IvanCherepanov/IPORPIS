import sys

from PyQt5.QtWidgets import QApplication

from tasks.task_2.email_app import EmailSenderApp


def main():
    app = QApplication(sys.argv)

    window = EmailSenderApp()
    window.setFixedSize(550, 800)
    window.setWindowTitle('EmailSenderApp')
    window.show()

    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
