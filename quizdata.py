"""
Класс, отвечающий за викторину.

quiz_data: dict, словарь где ключ - это вопрос викторины,
значение - это список со списком ответов и индексом верного ответа
"""
import random


class Quiz:
    def __init__(self):
        self.quiz_data = {
            "Марсельское таро и таро Райдера Уэйта - это одна и та же система?": [
                ["Верно", "Не верно"], 1
            ],
            "Какой из Арканов предвещает скорое замужество?": [
                ["Прямая императрица", "Перевёрнутая императрица", "Четверка кубков"], 0
            ],
            "Состоится ли свадьба по четвёрке жезлов?": [
                ["Да", "Нет", "Состоится, но не скоро"], 0
            ],
            "Какой из перечисленных Арканов говорит о мудрости?": [
                ["Десятка кубков", "Отшельник", "Колесо фортуны"], 1
            ],
            "На опасность на дороге укажет связка Арканов:": [
                ["Император + туз жезлов", "Восемь кубков + туз кубков", "Колесница + 10 мечей"], 2
            ],
            "Будет ли беременность в загаданный срок по перевёрнутой императрице?": [
               ["Да", "Нет"], 1
            ],
            "Кто из рыцарей самый романтичный?": [
                ["Рыцарь кубков", "Рыцарь жезлов", "Рыцарь мечей", "Рыцарь пентаклей"], 0
            ],
            "Какая из королев наиболее харизматичная?": [
                ["Королева пентаклей", "Королева жезлов", "Королева кубков", "Королева мечей"], 1
            ],
            "Какая из перечисленных связок укажет на измену?": [
                ["Влюблённые + двойка кубков", "Туз кубков + туз жезлов", "Дьявол + пятерка мечей"], 2
            ],
            "На переезд укажет": [
                ["Колесница", "Туз пентаклей", "Тройка пентаклей"], 0
            ],
            "На девичник укажет": [
                ["Туз мечей", "Тройка пентаклей", "Тройка кубков"], 2
            ]
        }

    def shuffle_questions(self):
        """
        Функция случайно перемешивает вопросы викторины.

        :return: list[str], список с рандомно перемешанными вопросами викторины
        """

        questions = list(self.quiz_data.keys())
        random.shuffle(questions)
        return questions

    def get_answers(self, question):
        """
        Функция возвращает список ответов на вопрос question

        :param question: str, вопрос викторины (равен одному из ключей quiz_data)
        :return: list[str], список с ответами на вопрос question
        """

        answers = self.quiz_data[question][0]
        return answers

    def get_correct_question(self, question):
        """
        Функция возвращает индекс корректного ответа на вопрос question

        :param question: str, вопрос викторины (равен одному из ключей quiz_data)
        :return: int, индекс верного ответа
        """
        correct_question = self.quiz_data[question][1]
        return correct_question
