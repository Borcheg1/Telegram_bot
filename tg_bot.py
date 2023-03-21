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


WEBINAR_DATE = datetime.strptime("2023 3 23 20:00", "%Y %m %d %H:%M")  # установите время в формате год, месяц, день, час, минута
                                                                       # например WEBINAR_DATE = datetime.strptime("2023 3 20 16:15", "%Y %m %d %H:%M")
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


@dp.message_handler(filters.Regexp(regexp=r'(Р|р)егистрация'))
async def registration(message: types.Message):
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


@dp.message_handler()
async def message_handler(message: types.Message):
    """
    ================================
    ==    REGISTRATION HANDLER    ==
    ================================
    """

    id = message.from_id
    reg_answer = (
        f"Спасибо за регистрацию на вебинар! 👍\n"
        f"Жду тебя {dt.get_webinar_date()}!\n"
        f"_Ссылка на вебинар будет отправлена в этот чат и на почту за 10 минут до его начала, не пропусти!_"
    )

    try:
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
                        reply_markup=btn.verification_keyboard
                    )
                except Exception as error:
                    logger.debug(f"{error}: id {id} (user didn't get verification message where showing his data)")

        elif bd.check_reg_status(id) == "Verification" and message.text == 'Да ✅':
            try:
                bd.set_reg_status(id, "Registered")
            except Exception as error:
                logger.debug(f"{error}: id {id} (query set_reg_status didn't work)")

            try:
                await bot.send_message(id, reg_answer, parse_mode="Markdown", reply_markup=btn.menu_keyboard)
            except Exception as error:
                logger.debug(f"{error}: id {id} (user didn't get message after registration and accept his data)")

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

        elif bd.check_reg_status(id) == "Registered" and message.text == 'Изменить данные ✍':
            try:
                bd.set_reg_status(id, "Set name")
            except Exception as error:
                logger.debug(f"{error}: id {id} (query set_reg_status didn't work)")

            try:
                await bot.send_message(id, f"Введите свое имя или никнейм")
            except Exception as error:
                logger.debug(f"{error}: id {id} (user couldn't change data after registration (set name))")

        elif bd.check_reg_status(id) == "Registered" and message.text == 'Оставить без изменений ✋':
            try:
                await bot.send_message(id, f"Ваши данные остались без изменений", reply_markup=btn.menu_keyboard)
            except Exception as error:
                logger.debug(f"{error}: id {id} (user didn't get message after reject to change his data)")

        """
        ================================
        ==        QUIZ HANDLER        ==
        ================================
        """

        if message.text == "Викторина 🎮" and bd.check_reg_status(id) != "Registered":
            try:
                await bot.send_message(id, "Пожалуйста, зарегистрируйтесь!", reply_markup=btn.menu_keyboard)
            except Exception as error:
                logger.debug(f"{error}: id {id} (user didn't get message about need to registration before quiz)")

        elif message.text == "Викторина 🎮" and bd.check_reg_status(id) == "Registered":
            try:
                bd.set_quiz_score(id, "-1, 0, 0")
            except Exception as error:
                logger.debug(f"{error}: id {id} (query set_quiz_score didn't work)")

            try:
                await quiz(id)
            except Exception as error:
                logger.debug(f"{error}: id {id} (quiz hasn't start)")

        """
        ================================
        ==       PRICE HANDLER        ==
        ================================
        """

        if message.text == "Цены 💰":
            pictures = os.listdir('price_pictures')
            media = types.MediaGroup()
            for picture in pictures:
                media.attach_photo(types.InputFile(f"price_pictures/{picture}"), picture)
            try:
                await bot.send_message(id, f"Загружаю...")
                await bot.send_media_group(id, media=media)
            except Exception as error:
                logger.debug(f"{error}: id {id} (user didn't get price pictures)")

    except Exception as error:
        logger.debug(f"{error}: id {id} (problem with bd queries check_reg_status into message_handler)")


async def quiz(id, answer=None):
    start_answer = (
        f"❓ Викторина состоит из 11 вопросов ❓\n"
        f"Проверим, как хорошо вы знакомы с таро?"
    )

    if answer is None:
        try:
            msg = await bot.send_poll(
                        id,
                        start_answer,
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
                answer,
                qz.get_questions(answer),
                type='quiz',
                correct_option_id=qz.get_correct_question(answer),
                is_anonymous=False
            )
        except Exception as error:
            logger.debug(f"{error}: id {id} (didn't send next quiz question)")

        try:
            bd.set_quiz_status(id, msg.poll.id)
        except Exception as error:
            logger.debug(f"{error}: id {id} (query set_quiz_status didn't work)")


@dp.poll_answer_handler()
async def poll_answer_handler(quiz_answer: types.PollAnswer):
    id = quiz_answer.user.id
    poll_id = quiz_answer.poll_id

    try:
        if poll_id == bd.get_quiz_status(id):

            quiz_stage, quiz_score, correct_answer = bd.get_quiz_score(id).split(', ')
            quiz_stage, quiz_score, correct_answer = int(quiz_stage), int(quiz_score), int(correct_answer)

            if quiz_stage < 10:

                if quiz_stage == -1 and quiz_answer.option_ids[0] == correct_answer:
                    answers = qz.shuffle_answers()
                    try:
                        bd.set_quiz_answers(id, '#'.join(answers))
                    except Exception as error:
                        logger.debug(f"{error}: id {id} (query set_quiz_answers didn't work)")

                    quiz_stage += 1
                    correct_answer = qz.get_correct_question(answers[quiz_stage])
                    try:
                        bd.set_quiz_score(id, f"{quiz_stage}, {quiz_score}, {correct_answer}")
                    except Exception as error:
                        logger.debug(f"{error}: id {id} (query set_quiz_score didn't work)")

                    try:
                        await quiz(id, answers[quiz_stage])
                    except Exception as error:
                        logger.debug(f"{error}: id {id} (didn't send first quiz question)")

                elif quiz_stage == -1 and quiz_answer.option_ids[0] != correct_answer:
                    try:
                        bd.set_quiz_status(id, "Cancelled")
                    except Exception as error:
                        logger.debug(f"{error}: id {id} (query set_quiz_status didn't work)")

                    try:
                        await bot.send_message(id, "Проверьте свои знания в следующий раз!", reply_markup=btn.menu_keyboard)
                    except Exception as error:
                        logger.debug(f"{error}: id {id} (user didn't get message after reject quiz)")

                else:
                    if quiz_answer.option_ids[0] == correct_answer:
                        quiz_score += 1

                    quiz_stage += 1
                    answers = bd.get_quiz_answers(id).split('#')
                    next_answer = answers[quiz_stage]
                    correct_answer = qz.get_correct_question(next_answer)
                    try:
                        bd.set_quiz_score(id, f"{quiz_stage}, {quiz_score}, {correct_answer}")
                    except Exception as error:
                        logger.debug(f"{error}: id {id} (query set_quiz_score didn't work)")

                    try:
                        await quiz(id, next_answer)
                    except Exception as error:
                        logger.debug(f"{error}: id {id} (didn't send next quiz question)")

            else:
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


if __name__ == '__main__':
    scheduler.add_job(
        reminder,
        'interval',
        hours=24, start_date='2023-03-20 12:00:00',
        end_date=WEBINAR_DATE,
        timezone='Europe/Moscow'
    )

    # scheduler.add_job(
    #     news_place,
    #     'date',
    #     run_date=datetime(2023, 3, 23, 16),
    #     timezone='Europe/Moscow'
    # )

    scheduler.start()
    executor.start_polling(dp, skip_updates=True)
