import psycopg2
from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QMessageBox
from psycopg2 import DatabaseError

from tasks.logger import logger


class DatabaseApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = uic.loadUi('files/database_app.ui', self)

        # Подключаем кнопки
        self.ui.connect_button.clicked.connect(self.connect_to_db)  # Подключение кнопки для добавления вложений
        self.ui.close_button.clicked.connect(self.close_action)
        self.ui.get_table_button.clicked.connect(self.get_tables)
        self.ui.do_request_button.clicked.connect(self.execute_action)

        self.actions_combo.addItems(["Выбрать данные из таблицы",
                                     "Вставить данные",
                                     "Удалить выбранную таблицу"]
                                    )

        # ДеАктивация элементов интерфейса
        self.get_table_button.setEnabled(False)
        self.do_request_button.setEnabled(False)
        self.combo_table_box.setEnabled(False)
        self.do_request_button.setEnabled(False)
        self.actions_combo.setEnabled(False)

        # Переменные для соединения
        self.conn = None
        self.cursor = None

    def connect_to_db(self):
        # Закрытие предыдущего соединения, если оно есть
        if self.conn:
            self.conn.close()
        try:
            # Получение данных из полей ввода
            host = self.host_input.text() or "127.0.0.1"
            port = self.port_input.text() or "5435"

            user = self.login_input.text() or "backend-tg-user"
            password = self.pass_input.text() or "backend-tg-pass"

            dbname = self.db_name_input.text() or "backend-tg"
        except Exception as e:
            logger.exception(e)

        try:
            if user == "" or password == "" or dbname == "" or host == "" or port == "":
                QMessageBox.warning(self, "Предупреждение", "Введите данные подключения")
                return

            # Попытка подключения
            self.conn = psycopg2.connect(
                dbname=dbname,
                user=user,
                password=password,
                host=host,
                port=port
            )
            self.cursor = self.conn.cursor()
            self.ui.result_output.setText("Подключение успешно установлено")

            # Активация элементов интерфейса
            self.get_table_button.setEnabled(True)
            self.do_request_button.setEnabled(True)
            self.combo_table_box.setEnabled(True)
            self.do_request_button.setEnabled(True)
            self.actions_combo.setEnabled(True)

        except psycopg2.Error as e:
            logger.exception(e)
            QMessageBox.critical(self, "Ошибка подключения", f"Не удалось подключиться: {str(e)}")
            self.conn = None
            self.cursor = None
        except Exception as e:
            logger.exception(e)
            QMessageBox.critical(self, "Ошибка", f"Произошла ошибка: {str(e)}")

    def get_tables(self):
        logger.debug("start process")
        if not self.conn:
            QMessageBox.warning(self, "Предупреждение", "Сначала подключитесь к базе данных")
            return
        try:
            self.combo_table_box.clear()
            self.cursor.execute("SELECT table_name FROM information_schema.tables WHERE table_schema='public';")
            tables = self.cursor.fetchall()
            for table in tables:
                self.combo_table_box.addItem(table[0])
            logger.debug("end process")
        except DatabaseError as e:
            self.conn.rollback()  # Откат транзакции
            QMessageBox.critical(self, "Ошибка", f"Ошибка при получении таблиц: {str(e)}. Транзакция откатана.")
        except psycopg2.Error as e:
            logger.exception(e)
            QMessageBox.critical(self, "Ошибка", f"Ошибка при получении таблиц: {str(e)}")
        except Exception as e:
            logger.exception(e)
            QMessageBox.critical(self, "Ошибка", f"Произошла ошибка: {str(e)}")

    def execute_action(self):
        if not self.conn:
            QMessageBox.warning(self, "Предупреждение", "Сначала подключитесь к базе данных")
            return

        action = self.actions_combo.currentText()
        table = self.combo_table_box.currentText()
        input_text = self.sql_request_input.toPlainText()

        try:
            if action == "Выбрать данные из таблицы":
                query = input_text if input_text else f"SELECT * FROM {table}"
                self.cursor.execute(query)
                results = self.cursor.fetchall()
                self.sql_response_output.setText(str(results))

            elif action == "Вставить данные":
                if input_text:
                    values = [val.strip() for val in input_text.split(',')]
                    placeholders = ','.join(['%s' for _ in values])
                    query = f"INSERT INTO {table} VALUES (DEFAULT, {placeholders})"
                    self.cursor.execute(query, values)
                    self.conn.commit()
                    self.sql_response_output.setText("Данные успешно вставлены")
                else:
                    self.sql_response_output.setText("Введите данные для вставки")

            elif action == "Удалить выбранную таблицу":
                self.cursor.execute(f"DROP TABLE IF EXISTS {table} CASCADE")
                self.conn.commit()
                self.sql_response_output.setText(f"Таблица {table} удалена")
                self.get_tables()
        except DatabaseError as e:
            self.conn.rollback()  # Откат транзакции при aborted состоянии
            if "current transaction is aborted" in str(e):
                QMessageBox.critical(self, "Ошибка",
                                     "Транзакция прервана из-за предыдущей ошибки. "
                                     "Транзакция откатана, повторите операцию.")
            else:
                QMessageBox.critical(self, "Ошибка", f"Ошибка базы данных: {str(e)}. Транзакция откатана.")

        except psycopg2.Error as e:
            logger.exception(e)
            QMessageBox.critical(self, "Ошибка", f"Ошибка базы данных: {str(e)}")
        except Exception as e:
            logger.exception(e)
            QMessageBox.critical(self, "Ошибка", f"Произошла ошибка: {str(e)}")

    def close_action(self):
        try:
            if self.conn:
                self.conn.close()
            # ДеАктивация элементов интерфейса
            self.combo_table_box.clear()
            self.get_table_button.setEnabled(False)
            self.do_request_button.setEnabled(False)
            self.combo_table_box.setEnabled(False)
            self.do_request_button.setEnabled(False)
            self.actions_combo.setEnabled(False)
        except Exception as e:
            logger.exception(e)
