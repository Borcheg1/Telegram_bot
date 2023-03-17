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

    def shuffle_answers(self):
        answers = list(self.quiz_data.keys())
        random.shuffle(answers)
        return answers

    def get_questions(self, answer):
        questions = self.quiz_data[answer][0]
        return questions

    def get_correct_question(self, answer):
        correct_question = self.quiz_data[answer][1]
        return correct_question
