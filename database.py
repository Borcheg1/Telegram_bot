import psycopg2

import os


class DataBasePostgres:
    """
    Переменные окружения в конструкторе берутся с сервиса RailWay при деплое приложения.
    При использовании локальной БД или другого сервиса, задайте эти переменные окружения.
    """
    def __init__(self):
        self.connection = psycopg2.connect(
            database=os.environ["PGDATABASE"],
            user=os.environ["PGUSER"],
            password=os.environ["PGPASSWORD"],
            host=os.environ["PGHOST"],
            port=os.environ["PGPORT"]
        )
        self.cursor = self.connection.cursor()

    def add_user(self, user_id):
        with self.connection:
            self.cursor.execute("INSERT INTO users (user_id) VALUES (%s)", (user_id,))

    def check_user_exist(self, user_id):
        with self.connection:
            self.cursor.execute("SELECT user_id FROM users WHERE user_id = (%s)", (user_id,))
            return bool(len(self.cursor.fetchall()))

    def set_reg_status(self, user_id, reg_status):
        with self.connection:
            self.cursor.execute("UPDATE users SET reg_status = (%s) WHERE user_id = (%s)", (reg_status, user_id,))

    def check_reg_status(self, user_id):
        with self.connection:
            self.cursor.execute("SELECT reg_status FROM users WHERE user_id = (%s)", (user_id,))
            return self.cursor.fetchone()[0]

    def set_name(self, user_id, name):
        with self.connection:
            self.cursor.execute("UPDATE users SET name = (%s) WHERE user_id = (%s)", (name, user_id,))

    def get_name(self, user_id):
        with self.connection:
            self.cursor.execute("SELECT name FROM users WHERE user_id = (%s)", (user_id,))
            return self.cursor.fetchone()[0]

    def set_email(self, user_id, email):
        with self.connection:
            self.cursor.execute("UPDATE users SET email = (%s) WHERE user_id = (%s)", (email, user_id,))

    def get_email(self, user_id):
        with self.connection:
            self.cursor.execute("SELECT email FROM users WHERE user_id = (%s)", (user_id,))
            return self.cursor.fetchone()[0]

    def set_quiz_status(self, user_id, quiz_status):
        with self.connection:
            self.cursor.execute("UPDATE users SET quiz_status = (%s) WHERE user_id = (%s)", (quiz_status, user_id,))

    def get_quiz_status(self, user_id):
        with self.connection:
            self.cursor.execute("SELECT quiz_status FROM users WHERE user_id = (%s)", (user_id,))
            return self.cursor.fetchone()[0]
