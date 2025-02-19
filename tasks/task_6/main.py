import sys

from PyQt5.QtWidgets import QApplication

from tasks.task_6.text_editor_app import TextEditorApp


def main():
    app = QApplication(sys.argv)

    window = TextEditorApp()
    window.setFixedSize(800, 700)
    window.setWindowTitle('TextEditorApp')
    window.show()

    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
