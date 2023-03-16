from aiogram import Bot, Dispatcher, executor, filters, types
from dotenv import load_dotenv

import os
from database import DataBasePostgres
import buttons as btn
from quizdata import Quiz


load_dotenv()

bot = Bot(os.environ["TOKEN"])
dp = Dispatcher(bot)

bd = DataBasePostgres()


@dp.message_handler(commands="start")
async def start(message: types.Message):
    id = message.from_id
    answer = (
        f"*Приветствую!* 🌸\n\n"
        f"Рада вашему интересу к Таро! Приглашаю на бесплатный вебинар «Обучение Таро. Система Райдера Уэйта».\n\n"
        f"*Вебинар состоится 23 марта в 20:00 по Московскому времени*\n"
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
        bd.add_user(id)

    await bot.send_message(id, answer, parse_mode="Markdown", reply_markup=btn.menu_keyboard)


@dp.message_handler(filters.Regexp(regexp=r'(Р|р)егистрация'))
async def registration(message: types.Message):
    id = message.from_id
    if bd.check_reg_status(id) == "Not registered":
        bd.set_reg_status(id, "Set name")
        await bot.send_message(id, "Введите свое имя или никнейм")

    elif bd.check_reg_status(id) == "Registered":
        await bot.send_message(
            id,
            f"Вы уже зарегистрированы под именем {bd.get_name(id)}\nХотите изменить свои данные?",
            reply_markup=btn.change_reg_keyboard
        )


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
        f"Жду тебя 23 марта в 20:00!\n"
        f"_Ссылка на вебинар будет отправлена в этот чат и на почту за 10 минут до его начала, не пропусти!_"
    )
    if bd.check_reg_status(id) == "Set name":
        if len(message.text) > 50:
            await message.reply("Имя не должно превышать 50 символов!")
        else:
            bd.set_name(id, message.text)
            bd.set_reg_status(id, "Set email")
            await bot.send_message(id, "Введите свою почту")

    elif bd.check_reg_status(id) == "Set email":
        if len(message.text) > 50 or "@" not in message.text:
            await message.reply("Почта должна содержать символ '@' и не превышать 50 символов!")
        else:
            bd.set_email(id, message.text)
            bd.set_reg_status(id, "Verification")
            await bot.send_message(
                id,
                f"Ваше имя: {bd.get_name(id)}\nВаша почта: {bd.get_email(id)}",
                reply_markup=btn.verification_keyboard
            )

    elif bd.check_reg_status(id) == "Verification" and message.text == 'Да ✅':
        bd.set_reg_status(id, "Registered")
        await bot.send_message(id, reg_answer, parse_mode="Markdown", reply_markup=btn.menu_keyboard)

    elif bd.check_reg_status(id) == "Verification" and message.text == 'Нет ❌':
        bd.set_reg_status(id, "Not registered")
        await bot.send_message(
            id,
            f"Чтобы пройти регистрацию заново нажми кнопку 'Регистрация'",
            reply_markup=btn.menu_keyboard
        )

    elif bd.check_reg_status(id) == "Registered" and message.text == 'Изменить данные ✍':
        bd.set_reg_status(id, "Set name")
        await bot.send_message(id, f"Введите свое имя или никнейм")

    elif bd.check_reg_status(id) == "Registered" and message.text == 'Оставить без изменений ✋':
        await bot.send_message(id, f"Ваши данные остались без изменений", reply_markup=btn.menu_keyboard)

    """
    ================================
    ==        QUIZ HANDLER        ==
    ================================
    """

    if message.text == "Викторина 🎮" and bd.check_reg_status(id) != "Registered":
        await bot.send_message(id, "Пожалуйста, зарегистрируйтесь!", reply_markup=btn.menu_keyboard)

    elif message.text == "Викторина 🎮" and bd.check_reg_status(id) == "Registered":
        bd.set_quiz_score(id, "0, 0, 0")
        await quiz(id)


async def quiz(id, answer=None):
    start_answer = (
        f"❓ Викторина состоит из 11 вопросов ❓\n"
        f"Проверим, как хорошо вы знакомы с таро?"
    )

    if answer is None:
        msg = await bot.send_poll(
                    id,
                    start_answer,
                    ['Начать ✅', 'Отменить ❌'],
                    type='quiz',
                    correct_option_id=0,
                    is_anonymous=False
                )

        bd.set_quiz_status(id, msg.poll.id)

    else:
        msg = await bot.send_poll(
            id,
            answer[0],
            answer[1][0],
            type='quiz',
            correct_option_id=answer[1][1],
            is_anonymous=False
        )

        bd.set_quiz_status(id, msg.poll.id)


@dp.poll_answer_handler()
async def poll_answer_handler(quiz_answer: types.PollAnswer):
    id = quiz_answer.user.id
    q = Quiz()
    poll_id = quiz_answer.poll_id

    if poll_id == bd.get_quiz_status(id):
        quiz_stage, quiz_score, correct_answer = bd.get_quiz_score(id).split(', ')
        quiz_stage, quiz_score, correct_answer = int(quiz_stage), int(quiz_score), int(correct_answer)

        if quiz_stage != 12:

            if quiz_stage == 0 and quiz_answer.option_ids[0] == correct_answer:
                answer = q.random_answer()
                quiz_stage += 1
                bd.set_quiz_score(id, f"{quiz_stage}, {quiz_score}, {answer[1][1]}")
                await quiz(id, answer)

            elif quiz_stage == 0 and quiz_answer.option_ids[0] != correct_answer:
                bd.set_quiz_status(id, "Cancelled")
                await bot.send_message(id, "Проверьте свои знания в следующий раз!", reply_markup=btn.menu_keyboard)

            elif quiz_answer.option_ids[0] == correct_answer:
                quiz_stage += 1
                quiz_score += 1
                answer = q.random_answer()
                bd.set_quiz_score(id, f"{quiz_stage}, {quiz_score}, {answer[1][1]}")
                await quiz(id, answer)

            elif quiz_answer.option_ids[0] != correct_answer:
                quiz_stage += 1
                answer = q.random_answer()
                bd.set_quiz_score(id, f"{quiz_stage}, {quiz_score}, {answer[1][1]}")
                await quiz(id, answer)

        else:
            await bot.send_message(
                id,
                f"Поздравляю! 👏\n"
                f"Верных ответов {quiz_score} из 11"
            )

            bd.set_quiz_status(id, "Cancelled")


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)



# {"message_id": 370,
#  "from": {
#     "id": 6273275670,
#     "is_bot": true,
#     "first_name": "test_bot",
#     "username": "test_borcheg_bot"
# },
#  "chat":{
#      "id": 1389025459,
#      "first_name": "Borcheg",
#      "type": "private"
#  },
#  "date": 1678993918,
#  "poll": {
#      "id": "5231373937232839491",
#      "question": "Какой из Арканов предвещает скорое замужество?",
#      "options": [
#          {"text": "Прямая императрица", "voter_count": 0},
#          {"text": "Перевёрнутая императрица", "voter_count": 0},
#          {"text": "Четверка кубков", "voter_count": 0}
#      ],
#      "total_voter_count": 0,
#      "is_closed": false,
#      "is_anonymous": false,
#      "type": "quiz",
#      "allows_multiple_answers": false,
#      "correct_option_id": 0}
#  }

