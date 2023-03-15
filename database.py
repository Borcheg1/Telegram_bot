import psycopg2

import os


class DataBasePostgres:
    """
    Переменные окружения в конструкторе берутся с сервиса RailWay при деплое приложения
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
            return self.cursor.execute("INSERT INTO users (user_id) VALUE (%s)", (user_id,))

    # def check_user_exist(self, user_id):
    #     with self.connection:
    #         result = self.cursor.execute("SELECT * FROM users WHERE user_id = (%s)", (user_id,)).fetchall()
    #         return bool(len(result))

    def set_reg_status(self, user_id, reg_status):
        with self.connection:
            return self.cursor.execute("UPDATE users SET reg_status = (%s) WHERE user_id = (%s)", (reg_status, user_id,))

    def check_reg_status(self, user_id):
        with self.connection:
            result = self.cursor.execute("SELECT reg_status FROM users WHERE user_id = (%s)", (user_id,))
            return bool(result)

    def set_name(self, user_id, name):
        with self.connection:
            return self.cursor.execute("UPDATE users SET name = (%s) WHERE user_id = (%s)", (name, user_id,))

    def set_email(self, user_id, email):
        with self.connection:
            return self.cursor.execute("UPDATE users SET email = (%s) WHERE user_id = (%s)", (email, user_id,))
