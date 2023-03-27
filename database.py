"""
Используется база данных PostgreSQL.
Класс, отвечающий за все запросы к базе данных.
"""
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

    def create_table(self):
        """
        Создание таблицы, если таблицы с таким названием не существует.

        :return: None
        """
        with self.connection:
            self.cursor.execute(
                "CREATE TABLE IF NOT EXISTS users ("
                "id serial PRIMARY KEY,"
                "user_id INTEGER UNIQUE NOT NULL,"
                "name VARCHAR (50),"
                "email VARCHAR (50),"
                "reg_status VARCHAR (20),"
                "del_status VARCHAR (20),"
                "quiz_status VARCHAR (20),"
                "quiz_score VARCHAR (20),"
                "quiz_questions TEXT[])"
            )

    def add_user(self, user_id):
        """
        Добавление id пользователя.

        :param user_id: int, id пользователя
        :return: None
        """

        with self.connection:
            self.cursor.execute("INSERT INTO users (user_id) VALUES (%s)", (user_id,))

    def delete_user(self, user_id):
        """
        Удаление id пользователя.

        :param user_id: int, id пользователя
        :return: None
        """

        with self.connection:
            self.cursor.execute("DELETE FROM users WHERE user_id = (%s)", (user_id,))
    
    def get_users_ids(self):
        """
        Получение id всех пользователей.

        :param user_id: int, id пользователя
        :return: list
        """

        with self.connection:
            self.cursor.execute("SELECT user_id FROM users")
            return self.cursor.fetchall()

    def check_user_exist(self, user_id):
        """
        Проверка есть ли пользователь в базе данных

        :param user_id: int, id пользователя
        :return: bool
        """
        with self.connection:
            self.cursor.execute("SELECT user_id FROM users WHERE user_id = (%s)", (user_id,))
            return bool(len(self.cursor.fetchall()))

    def set_reg_status(self, user_id, reg_status):
        """
        Изменение статуса регистрации пользователя

        :param user_id: int, id пользователя
        :param reg_status: str, статус регистрации пользователя
        :return: None
        """

        with self.connection:
            self.cursor.execute("UPDATE users SET reg_status = (%s) WHERE user_id = (%s)", (reg_status, user_id,))

    def set_del_status(self, user_id, del_status):
        """
        Изменение статуса удаления пользователя

        :param user_id: int, id пользователя
        :param reg_status: str, статус удаления пользователя
        :return: None
        """

        with self.connection:
            self.cursor.execute("UPDATE users SET del_status = (%s) WHERE user_id = (%s)", (del_status, user_id,))

    def check_reg_status(self, user_id):
        """
        Получение текущего статуса регистрации пользователя

        :param user_id: int, id пользователя
        :return: str, текущий статус регистрации пользователя
        """

        with self.connection:
            self.cursor.execute("SELECT reg_status FROM users WHERE user_id = (%s)", (user_id,))
            return self.cursor.fetchone()[0]

    def check_del_status(self, user_id):
        """
        Получение текущего статуса удаления пользователя

        :param user_id: int, id пользователя
        :return: str, текущий статус удаления пользователя
        """

        with self.connection:
            self.cursor.execute("SELECT del_status FROM users WHERE user_id = (%s)", (user_id,))
            return self.cursor.fetchone()[0]

    def set_name(self, user_id, name):
        """
        Изменение имени пользователя

        :param user_id: int, id пользователя
        :param name: str, имя пользователя
        :return: None
        """

        with self.connection:
            self.cursor.execute("UPDATE users SET name = (%s) WHERE user_id = (%s)", (name, user_id,))

    def get_name(self, user_id):
        """
        Получение текущего имени пользователя

        :param user_id: int, id пользователя
        :return: str, имя пользователя
        """

        with self.connection:
            self.cursor.execute("SELECT name FROM users WHERE user_id = (%s)", (user_id,))
            return self.cursor.fetchone()[0]

    def set_email(self, user_id, email):
        """
        Изменение пачты пользователя

        :param user_id: int, id пользователя
        :param name: str, почта пользователя
        :return: None
        """

        with self.connection:
            self.cursor.execute("UPDATE users SET email = (%s) WHERE user_id = (%s)", (email, user_id,))

    def get_email(self, user_id):
        """
        Получение текущей почты пользователя

        :param user_id: int, id пользователя
        :return: str, почта пользователя
        """

        with self.connection:
            self.cursor.execute("SELECT email FROM users WHERE user_id = (%s)", (user_id,))
            return self.cursor.fetchone()[0]

    def set_quiz_status(self, user_id, quiz_status):
        """
        Изменение статуса викторины

        :param user_id: int, id пользователя
        :param quiz_status: str, статус викторины (либо id викторины, либо 'Cancelled')
        :return: None
        """

        with self.connection:
            self.cursor.execute("UPDATE users SET quiz_status = (%s) WHERE user_id = (%s)", (quiz_status, user_id,))

    def get_quiz_status(self, user_id):
        """
        Получение текущего статуса викторины

        :param user_id: int, id пользователя
        :return: str, статус викторины (либо id викторины, либо 'Cancelled')
        """

        with self.connection:
            self.cursor.execute("SELECT quiz_status FROM users WHERE user_id = (%s)", (user_id,))
            return self.cursor.fetchone()[0]

    def set_quiz_score(self, user_id, quiz_score):
        with self.connection:
            self.cursor.execute("UPDATE users SET quiz_score = (%s) WHERE user_id = (%s)", (quiz_score, user_id,))

    def get_quiz_score(self, user_id):
        with self.connection:
            self.cursor.execute("SELECT quiz_score FROM users WHERE user_id = (%s)", (user_id,))
            return self.cursor.fetchone()[0]

    def set_quiz_questions(self, user_id, answers):
        """
        Изменение вопросов викторины

        :param user_id: int, id пользователя
        :param answers: list, список вопросов (модуль quizdata, класс Quiz, ключи словаря quiz_data)
        :return: None
        """

        self.cursor.execute("UPDATE users SET quiz_questions = (%s) WHERE user_id = (%s)", (answers, user_id,))

    def get_quiz_questions(self, user_id, question_number):
        """
        Получение текущих вопросов викторины

        :param user_id: int, id пользователя
        :return: list, список вопросов (модуль quizdata, класс Quiz, ключи словаря quiz_data)
        """
        
        self.cursor.execute("SELECT quiz_questions[(%s)] FROM users WHERE user_id = (%s)", (question_number, user_id,))
        return self.cursor.fetchone()[0]
