"""
Телеграмм бот, с функционалом регистрации и удаления пользователя, квизом, рассылкой картинок и
напоминанием об определенном событии. Так же присутствует возможность рассылки новостей по графику.

В дериктории проекта должна находиться папка с названием 'price_pictures',
в которой должны находиться не более 10 изображений с расширениями 'jpeg', 'jpg', 'png'.
В названии изображений не должно быть лишних знаков '.'
При вводе пользователем команды 'Цены 💰', ему будут отправлены эти изображения.
"""

import asyncio
from datetime import datetime
import os

from aiogram import Bot, Dispatcher, executor, filters, types
from dotenv import load_dotenv
from loguru import logger
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from database import DataBasePostgres
import buttons as btn
from quizdata import Quiz
from dates import Date


# установите время в формате год, месяц, день, час, минута
# например WEBINAR_DATE = datetime.strptime("2023 3 20 16:15", "%Y %m %d %H:%M")
WEBINAR_DATE = datetime.strptime("2023 3 28 20:00", "%Y %m %d %H:%M")
load_dotenv()

scheduler = AsyncIOScheduler()

logger.add(
    "log",
    format='{time} {level} {message}',
    level='DEBUG',
    rotation='1 week',
    compression='zip'
)

bot = Bot(os.environ["TOKEN"])
dp = Dispatcher(bot)

bd = DataBasePostgres()
bd.create_table()

qz = Quiz()

dt = Date(WEBINAR_DATE)


@dp.message_handler(commands="start")
async def start(message: types.Message):
    """
    Обработка команды '/start'.

    Функция для отправки приветственного сообщения при активации бота командой '/start'.

    Если пользователя нет в БД (столбец user_id), то записывает туда его ID.


    :param message: types.Message
    :return: None
    """

    id = message.from_id
    answer = (
        f"*Приветствую!* 🌸\n\n"
        f"Рада вашему интересу к Таро! Приглашаю на бесплатный вебинар «Обучение Таро. Система Райдера Уэйта».\n\n"
        f"*Вебинар состоится {dt.get_webinar_date()} по Московскому времени*\n"
        f"_Ссылка на вебинар будет отправлена в этот чат за 10 минут до его начала_\n\n"
        f"На вебинаре я расскажу:\n"
        f"• выбор колоды 🎴\n"
        f"• отличие систем таро и колод 🧐\n"
        f"• как правильно чистить колоды 🔥\n"
        f"• как верно читать карты  📖\n"
        f"• зачем нужны перевернутые карты и нужны ли? 🌚\n"
        f"• где искать первых клиентов 💰\n"
        f"• поделюсь собственными наработками 🧙\n"
        f"• проведём медитацию на Аркан таро 🧘‍♀️\n\n"
        f"Почему именно система Уэйта?\n"
        f"Данная система является классикой и обучившись на этой колоде, "
        f"вам будет легко работать с другими современными колодами.\n\n"
        f"Ставь будильник ⏰ и готовься конспектировать ✍️, "
        f"будет много полезного! До встречи на вебинаре! 🌷\n\n"
        f"Для приобретения обучения пишите по любому из контактов:\n\n"
        f"[Instagram](https://example.com)\n\n"
        f"[Telegram](https://t.me/test_borcheg_bot)\n\n"
    )

    if not bd.check_user_exist(id):
        try:
            bd.add_user(id)
        except Exception as error:
            logger.debug(f"{error}: id {id} (query add_user didn't work)")

    try:
        await bot.send_message(id, answer, parse_mode="Markdown", reply_markup=btn.menu_keyboard)
    except Exception as error:
        logger.debug(f"{error}: id {id} (user didn't get start message)")


@dp.message_handler(filters.Regexp(regexp=r'Регистрация 🎓'))
async def registration_handler(message: types.Message):
    """
    Обработка команды 'Регистрация 🎓'.

    Функция проверяет статус пользователя в БД (столбец reg_status).

    Если статус пользователя 'Registered', отправляет предупреждающее сообщение, что пользователь уже зарегистрирован
    и отправляет клавиатуру с запросом на изменение данных.

    Если статус не 'Registered', меняет статус на 'Set name' и отправляет сообщение о необходимости ввести имя.


    :param message: types.Message
    :return: None
    """

    id = message.from_id

    try:
        if bd.check_reg_status(id) == "Registered":
            try:
                await bot.send_message(
                    id,
                    f"Вы уже зарегистрированы под именем {bd.get_name(id)}\nХотите изменить свои данные?",
                    reply_markup=btn.change_reg_keyboard
                )
            except Exception as error:
                logger.debug(f"{error}: id {id} (user couldn't change his reg data)")

        else:
            try:
                bd.set_reg_status(id, "Set name")
            except Exception as error:
                logger.debug(f"{error}: id {id} (set_name query didn't work)")

            try:
                await bot.send_message(id, "Введите свое имя или никнейм", reply_markup=types.ReplyKeyboardRemove())
            except Exception as error:
                logger.debug(f"{error}: id {id} (user couldn't set name)")

    except Exception as error:
        logger.debug(f"{error}: id {id} (check_reg_status query didn't work)")


@dp.message_handler(filters.Regexp(regexp=r'Викторина 🎮'))
async def quiz_handler(message: types.Message):
    """
    Обработка команды 'Викторина 🎮'.

    Функция проверяет статус пользователя в БД (столбец reg_status).

    Если статус пользователя не 'Registered', отправляет сообщение о необходимости регистрации
    перед прохождением викторины.

    Если статус пользователя 'Registered', обновляет счет викторины (столбец quiz_score в БД)
    до начальных значений и вызывает функцию quiz().


    :param message: types.Message
    :return: None
    """

    id = message.from_id

    try:
        if bd.check_reg_status(id) != "Registered":
            try:
                await bot.send_message(id, "Пожалуйста, зарегистрируйтесь!", reply_markup=btn.menu_keyboard)
            except Exception as error:
                logger.debug(f"{error}: id {id} (user didn't get message about need to registration before quiz)")

        elif bd.check_reg_status(id) == "Registered":
            try:
                bd.set_quiz_score(id, "-1, 0, 0")
            except Exception as error:
                logger.debug(f"{error}: id {id} (query set_quiz_score didn't work)")

            try:
                await quiz(id)
            except Exception as error:
                logger.debug(f"{error}: id {id} (quiz hasn't start)")

    except Exception as error:
        logger.debug(f"{error}: id {id} (problem with bd queries check_reg_status into quiz_handler)")


@dp.message_handler(filters.Regexp(regexp=r'Цены 💰'))
async def price_handler(message: types.Message):
    """
    Обработка команды 'Цены 💰'.

    Функция находит все файлы в папке 'price_pictures', проверяет их расширения на соответствие 'jpeg', 'jpg', 'png',
    и добавляет в группу изображений MediaGroup до 10 изображений.

    Затем отправляет сообщение 'Загружаю...' и следом группу изображений.


    :param message: types.Message
    :return: None
    """

    id = message.from_id
    pictures = os.listdir('price_pictures')
    media = types.MediaGroup()
    for idx, picture in enumerate(pictures):
        if len(picture.split('.')) == 2 and picture.split('.')[1].lower() in ('jpeg', 'jpg', 'png') and idx < 10:
            media.attach_photo(types.InputFile(f"price_pictures/{picture}"), picture)
    try:
        await bot.send_message(id, f"Загружаю...")
        await bot.send_media_group(id, media=media)
    except Exception as error:
        logger.debug(f"{error}: id {id} (user didn't get price pictures)")


@dp.message_handler(filters.Regexp(regexp=r'Удаление ⛔'))
async def delete_handler(message: types.Message):
    """
    Обработка команды 'Удаление ⛔'.

    Функция обновляет статус удаления пользователя на 'Deleting' (столбец del_status в БД).

    Отправляет сообщение для подтверждения удаления пользователя и клавиатуру с кнопакми 'Да ✅', 'Нет ❌'.


    :param message: types.Message
    :return: None
    """

    id = message.from_id
    try:
        bd.set_del_status(id, "Deleting")
    except Exception as error:
        logger.debug(f"{error}: id {id} (query set_del_status didn't work)")

    try:
        await bot.send_message(
            id,
            "Вы уверены, что больше не хотите получать от меня сообщения?",
            reply_markup=btn.yes_no_keyboard
        )

    except Exception as error:
        logger.debug(f"{error}: id {id} (user didn't get message about delete his id)")


async def quiz(id, question=None):
    """
    Функция принимает параметр question: str (по умалчанию None) с вопросом викторины.

    Если параметр question равен None, то пользователь получает стартовый вопрос 'start_question' о начале викторины
    с ответами 'Начать ✅', 'Отменить ❌'.

    Если параметр question не равен None, то викторина уже в процессе и пользователь получает этап викторины
    с вопросом question.

    Меняется статус викторины пользователя на ID викторины (столбец quiz_status в БД).

    Вопросы, ответы и правильный ответ викторины берутся из модуля quizdata, класса Quiz.


    :param question: str, вопрос викторины
    :return: None
    """

    start_question = (
        f"❓ Викторина состоит из {len(qz.quiz_data)} вопросов ❓\n"
        f"Проверим, как хорошо вы знакомы с таро?"
    )

    if question is None:
        try:
            msg = await bot.send_poll(
                        id,
                        start_question,
                        ['Начать ✅', 'Отменить ❌'],
                        type='quiz',
                        correct_option_id=0,
                        is_anonymous=False
                    )
        except Exception as error:
            logger.debug(f"{error}: id {id} (didn't send first quiz question)")

        try:
            bd.set_quiz_status(id, msg.poll.id)
        except Exception as error:
            logger.debug(f"{error}: id {id} (query set_quiz_status didn't work)")

    else:
        try:
            msg = await bot.send_poll(
                id,
                question,
                qz.get_answers(question),
                type='quiz',
                correct_option_id=qz.get_correct_question(question),
                is_anonymous=False
            )
        except Exception as error:
            logger.debug(f"{error}: id {id} (didn't send next quiz question)")

        try:
            bd.set_quiz_status(id, msg.poll.id)
        except Exception as error:
            logger.debug(f"{error}: id {id} (query set_quiz_status didn't work)")


@dp.poll_answer_handler()
async def poll_answer_handler(quiz_question: types.PollAnswer):
    """
    Функция обрабатывает ответ пользователя на вопрос викторины.

    Выполняется запрос счета викторины (столбец quiz_score в БД),
    если quiz_stage равняется -1, то пользователь ответил на стартовый вопрос.

    Если ответ положительный, то в базу данных записываются все вопросы викторины
    в случайном порядке (столбец quiz_questions).

    Если ответ отрицательный, то викторина завершается
    и в базу данных записывается статус 'Cancelled' (столбец quiz_status).

    По окончании викторины отправляется сообщение с результатами.


    :param quiz_question: types.PollAnswer
    :return: None
    """

    id = quiz_question.user.id
    poll_id = quiz_question.poll_id

    try:
        # проверка относится ли викторина к пользователю
        if poll_id == bd.get_quiz_status(id):

            # получение счета викторины из бд
            # quiz_stage: str, этап викторины (порядковый номер вопроса). При значении -1 выдается стартовый вопрос
            # quiz_score: str, счетчик правильных ответов
            # correct_answer: str, индекс правильного ответа
            quiz_stage, quiz_score, correct_answer = bd.get_quiz_score(id).split(', ')
            quiz_stage, quiz_score, correct_answer = int(quiz_stage), int(quiz_score), int(correct_answer)

            # общее количество вопросов викторины
            if quiz_stage < len(qz.quiz_data) - 1:

                # если ответ на стартовый вопрос положительный, то вопросы рандомно перемешиваются
                # и записываются в базу данных (столбец quiz_questions)
                if quiz_stage == -1 and quiz_question.option_ids[0] == correct_answer:
                    questions = qz.shuffle_questions()
                    try:
                        bd.set_quiz_questions(id, questions)
                    except Exception as error:
                        logger.debug(f"{error}: id {id} (query set_quiz_questions didn't work)")

                    # увеличение порядкового номера вопроса, получение правильного ответа
                    # и обновление счета викторины в БД (столбец quiz_score)
                    quiz_stage += 1
                    correct_answer = qz.get_correct_question(questions[quiz_stage])
                    try:
                        bd.set_quiz_score(id, f"{quiz_stage}, {quiz_score}, {correct_answer}")
                    except Exception as error:
                        logger.debug(f"{error}: id {id} (query set_quiz_score didn't work)")

                    # вызов функции quiz с передачей следующего вопроса
                    try:
                        await quiz(id, questions[quiz_stage])
                    except Exception as error:
                        logger.debug(f"{error}: id {id} (didn't send first quiz question)")

                # если ответ на стартовый вопрос отрицательный, то викторина завершается
                # и обновляется статус викторины в БД на 'Cancelled' (столбец quiz_status)
                elif quiz_stage == -1 and quiz_question.option_ids[0] != correct_answer:
                    try:
                        bd.set_quiz_status(id, "Cancelled")
                    except Exception as error:
                        logger.debug(f"{error}: id {id} (query set_quiz_status didn't work)")

                    try:
                        await bot.send_message(id, "Проверьте свои знания в следующий раз!", reply_markup=btn.menu_keyboard)
                    except Exception as error:
                        logger.debug(f"{error}: id {id} (user didn't get message after reject quiz)")

                # обработка ответов на не стартовый вопрос
                else:
                    if quiz_question.option_ids[0] == correct_answer:
                        quiz_score += 1

                    # получение следующего вопроса из базы данных (PostgreSQL начинает индекс с 1)
                    # получение индекса правильного ответа
                    # обновление счета викторины в БД
                    # вызов функции quiz с передачей следующего вопроса
                    quiz_stage += 1
                    next_question = bd.get_quiz_questions(id, quiz_stage + 1)
                    correct_answer = qz.get_correct_question(next_question)
                    try:
                        bd.set_quiz_score(id, f"{quiz_stage}, {quiz_score}, {correct_answer}")
                    except Exception as error:
                        logger.debug(f"{error}: id {id} (query set_quiz_score didn't work)")

                    try:
                        await quiz(id, next_question)
                    except Exception as error:
                        logger.debug(f"{error}: id {id} (didn't send next quiz question)")

            # обработка завершения викторины
            else:
                if quiz_question.option_ids[0] == correct_answer:
                    quiz_score += 1
                try:
                    await bot.send_message(
                        id,
                        f"Поздравляю! 👏\n"
                        f"Верных ответов {quiz_score} из 11",
                        reply_markup=btn.menu_keyboard
                    )
                except Exception as error:
                    logger.debug(f"{error}: id {id} (user didn't get congrats message after quiz)")

                try:
                    bd.set_quiz_status(id, "Cancelled")
                except Exception as error:
                    logger.debug(f"{error}: id {id} (query set_quiz_status didn't work)")

    except Exception as error:
        logger.debug(f"{error}: id {id} (queries get_quiz_status into func poll_message_handler didn't work)")


async def reminder():
    """
    Функция напоминания о вебинаре.

    Используется модуль dates, класс Date.

    Отправляет всем пользователям из базы данных (столбец user_id) сообщение о количестве дней до начала вебинара.


    :return: None
    """

    try:
        users_ids = bd.get_users_ids()
    except Exception as error:
        logger.debug(f"{error}: (query get_users_ids didn't work)")

    days_left = dt.days_left()

    for id in users_ids:
        if id[0]:
            if days_left == "1 день":
                try:
                    await bot.send_message(id[0], f"❗ До вебинара остался {days_left} ❗")
                    await asyncio.sleep(0.05)
                except Exception as error:
                    logger.debug(f"{error}: id {id[0]} (user didn't get remind message)")
            elif days_left:
                try:
                    await bot.send_message(id[0], f"❗ До вебинара осталось {days_left} ❗")
                    await asyncio.sleep(0.05)
                except Exception as error:
                    logger.debug(f"{error}: id {id[0]} (user didn't get remind message)")
            else:
                try:
                    await bot.send_message(id[0], f"❗ Вебинар уже сегодня, не пропусти ❗")
                    await asyncio.sleep(0.05)
                except Exception as error:
                    logger.debug(f"{error}: id {id[0]} (user didn't get today remind message)")


async def news_place():
    """
    Функция для отправки новостей.

    Отправляет всем пользователям из базы данных (столбец user_id) сообщение.


    :return: None
    """

    try:
        users_ids = bd.get_users_ids()
    except Exception as error:
        logger.debug(f"{error}: (query get_users_ids didn't work)")

    news_message = (
        f"Здесь будут свежие новости"
    )

    for id in users_ids:
        if id[0]:
            try:
                await bot.send_message(id[0], news_message, parse_mode="Markdown")
                await asyncio.sleep(0.05)
            except Exception as error:
                logger.debug(f"{error}: id {id[0]} (user didn't get news message)")


@dp.message_handler()
async def message_handler(message: types.Message):
    """
    Обработка всех сообщений пользователя, за исключением сообщений
    'Регистрация 🎓', 'Викторина 🎮', 'Цены 💰', 'Удаление ⛔'.




    :param message: types.Message
    :return: None
    """

    id = message.from_id
    reg_answer = (
        f"Спасибо за регистрацию на вебинар! 👍\n"
        f"Жду тебя {dt.get_webinar_date()}!\n"
        f"_Ссылка на вебинар будет отправлена в этот чат и на почту за 10 минут до его начала, не пропусти!_"
    )

    """
    ================================
    ==    REGISTRATION HANDLER    ==
    ================================
    """

    try:
        # Если статус регистрации пользователя 'Set name' (столбец reg_status), то следующее сообщение,
        # за исключением командных, будет записано в базу данных как имя пользователя (столбец name).
        # Затем статус пользователя меняется на 'Set email'.
        if bd.check_reg_status(id) == "Set name":
            if len(message.text) > 50:
                try:
                    await message.reply("Имя не должно превышать 50 символов!")
                except Exception as error:
                    logger.debug(f"{error}: id {id} (user didn't get valid set name message)")

            else:
                try:
                    bd.set_name(id, message.text)
                except Exception as error:
                    logger.debug(f"{error}: id {id} (query set_name didn't work)")

                try:
                    bd.set_reg_status(id, "Set email")
                except Exception as error:
                    logger.debug(f"{error}: id {id} (query set_reg_status didn't work)")

                try:
                    await bot.send_message(id, "Введите свою почту")
                except Exception as error:
                    logger.debug(f"{error}: id {id} (user couldn't set email)")

        # Если статус регистрации пользователя 'Set email' (столбец reg_status), то следующее сообщение,
        # за исключением командных, будет записано в базу данных как почта пользователя (столбец email).
        # Затем статус пользователя меняется на 'Verification' и ожидается продтверждение
        # корректности введенных имени и почты от пользователя.
        elif bd.check_reg_status(id) == "Set email":
            if len(message.text) > 50 or "@" not in message.text:
                try:
                    await message.reply("Почта должна содержать символ '@' и не превышать 50 символов!")
                except Exception as error:
                    logger.debug(f"{error}: id {id} (user didn't get valid email message)")

            else:
                try:
                    bd.set_email(id, message.text)
                except Exception as error:
                    logger.debug(f"{error}: id {id} (query set_email didn't work)")
                try:
                    bd.set_reg_status(id, "Verification")
                except Exception as error:
                    logger.debug(f"{error}: id {id} (query set_reg_status didn't work)")

                try:
                    await bot.send_message(
                        id,
                        f"Ваше имя: {bd.get_name(id)}\nВаша почта: {bd.get_email(id)}",
                        reply_markup=btn.yes_no_keyboard
                    )
                except Exception as error:
                    logger.debug(f"{error}: id {id} (user didn't get verification message where showing his data)")

        # Если статус регистрации пользователя 'Verification' (столбец reg_status) и сообщение 'Да ✅', то
        # статус пользователя меняется на 'Registered'
        elif bd.check_reg_status(id) == "Verification" and message.text == 'Да ✅':
            try:
                bd.set_reg_status(id, "Registered")
            except Exception as error:
                logger.debug(f"{error}: id {id} (query set_reg_status didn't work)")

            try:
                await bot.send_message(id, reg_answer, parse_mode="Markdown", reply_markup=btn.menu_keyboard)
            except Exception as error:
                logger.debug(f"{error}: id {id} (user didn't get message after registration and accept his data)")

        # Если статус регистрации пользователя 'Verification' (столбец reg_status) и сообщение 'Нет ❌', то
        # статус пользователя меняется на 'Not registered' и отправляется сообщение о повторной регистрации.
        elif bd.check_reg_status(id) == "Verification" and message.text == 'Нет ❌':
            try:
                bd.set_reg_status(id, "Not registered")
            except Exception as error:
                logger.debug(f"{error}: id {id} (query set_reg_status didn't work)")

            try:
                await bot.send_message(
                    id,
                    f"Чтобы пройти регистрацию заново нажми кнопку 'Регистрация'",
                    reply_markup=btn.menu_keyboard
                )
            except Exception as error:
                logger.debug(f"{error}: id {id} (user didn't get message after registration and don't accept his data)")

        # Если статус регистрации пользователя 'Registered' (столбец reg_status) и сообщение 'Изменить данные ✍', то
        # статус пользователя меняется на 'Set name' и отправляется сообщение с предложением ввести имя.
        elif bd.check_reg_status(id) == "Registered" and message.text == 'Изменить данные ✍':
            try:
                bd.set_reg_status(id, "Set name")
            except Exception as error:
                logger.debug(f"{error}: id {id} (query set_reg_status didn't work)")

            try:
                await bot.send_message(id, f"Введите свое имя или никнейм")
            except Exception as error:
                logger.debug(f"{error}: id {id} (user couldn't change data after registration (set name))")

        # Если статус регистрации пользователя 'Registered' (столбец reg_status)
        # и сообщение 'Оставить без изменений ✋', то отправляется сообщение об отмене изменений.
        elif bd.check_reg_status(id) == "Registered" and message.text == 'Оставить без изменений ✋':
            try:
                await bot.send_message(id, f"Ваши данные остались без изменений", reply_markup=btn.menu_keyboard)
            except Exception as error:
                logger.debug(f"{error}: id {id} (user didn't get message after reject to change his data)")

    except Exception as error:
        logger.debug(f"{error}: id {id} (problem with bd queries check_reg_status into message_handler)")

    """
    ==========================
    ==    DELETE HANDLER    ==
    ==========================
    """

    try:
        # Если статус удаления пользователя 'Deleting' (столбец del_status) и сообщение 'Да ✅', то
        # отправляется сообщение о возможности возобнавления работы с ботом и удаляет пользователя из базы данных.
        if bd.check_del_status(id) == "Deleting" and message.text == "Да ✅":
            try:
                await bot.send_message(
                    id,
                    "Чтобы возобновить работу с ботом введите команду '/start'",
                    reply_markup=btn.start_keyboard
                )
            except Exception as error:
                logger.debug(f"{error}: id {id} (user didn't get message after accept deliting)")

            await asyncio.sleep(0.5)

            try:
                bd.delete_user(id)
            except Exception as error:
                logger.debug(f"{error}: id {id} (query delete_user didn't work; user wasn't delete from bd)")

        # Если статус удаления пользователя 'Deleting' (столбец del_status) и сообщение 'Нет ❌', то
        # отправляется сообщение с благодарностью и меняется статус удаления на 'Rejected'
        elif bd.check_del_status(id) == "Deleting" and message.text == "Нет ❌":
            try:
                await bot.send_message(id, "Спасибо, что продолжаете пользоваться ботом!", reply_markup=btn.menu_keyboard)
            except Exception as error:
                logger.debug(f"{error}: id {id} (user didn't get message after decline deliting)")

            try:
                bd.set_del_status(id, "Rejected")
            except Exception as error:
                logger.debug(f"{error}: id {id} (query set_del_status didn't work)")

    except Exception as error:
        logger.debug(f"{error}: id {id} (query check_del_status didn't work into message_handler)")


if __name__ == '__main__':
    # создание графика вызова функции reminder
    scheduler.add_job(
        reminder,
        'interval',
        minutes=1, start_date='2023-03-27 15:00:00',
        end_date=WEBINAR_DATE,
        timezone='Europe/Moscow'
    )

    # создание графика вызова функции news_place
    scheduler.add_job(
        news_place,
        'date',
        run_date=datetime(2023, 3, 25, 18, 4),
        timezone='Europe/Moscow'
    )

    scheduler.start()
    executor.start_polling(dp, skip_updates=True)
