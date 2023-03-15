from aiogram import Bot, Dispatcher, executor, filters, types
from dotenv import load_dotenv

import os
from database import DataBasePostgres
import buttons as btn


load_dotenv()

bot = Bot(os.getenv("TOKEN"))
dp = Dispatcher(bot)

bd = DataBasePostgres()

quiz_data = {
    "Марсельское таро и таро Райдера Уэйта - это одна и та же система?": [
        "Верно", "Не верно"
    ],
    "Какой из Арканов предвещает скорое замужество?": [
        "Прямая императрица", "Перевёрнутая императрица", "Четверка кубков"
    ],
    "Состоится ли свадьба по четвёрке жезлов?": [
        "Да", "Нет", "Состоится, но не скоро"
    ],
    "Какой из перечисленных Арканов говорит о мудрости?": [
        "Десятка кубков", "Отшельник", "Колесо фортуны"
    ],
    "На опасность на дороге укажет связка Арканов:": [
        "Император + туз жезлов", "Восемь кубков + туз кубков", "Колесница + 10 мечей"
    ],
    "Будет ли беременность в загаданный срок по перевёрнутой императрице?": [
        "Да", "Нет"
    ],
    "Кто из рыцарей самый романтичный?": [
        "Рыцарь кубков", "Рыцарь жезлов", "Рыцарь мечей", "Рыцарь пентаклей"
    ],
    "Какая из королев наиболее харизматичная?": [
        "Королева пентаклей", "Королева жезлов", "Королева кубков", "Королева мечей"
    ],
    "Какая из перечисленных связок укажет на измену?": [
        "Влюблённые + двойка кубков", "Туз кубков + туз жезлов", "Дьявол + пятерка мечей"
    ],
    "На переезд укажет": [
        "Колесница", "Туз пентаклей", "Тройка пентаклей"
    ],
    "На девичник укажет": [
        "Туз мечей", "Тройка пентаклей", "Тройка кубков"
    ]
}

quiz_answers = (None, 1, 0, 0, 1, 2, 1, 0, 1, 2, 0, 2)


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
async def bot_message(message: types.Message):
    id = message.from_id
    answer = (
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
        await bot.send_message(id, answer, parse_mode="Markdown")

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
        await bot.send_message(id, f"Ваши данные остались без изменений")

    else:
        await bot.send_message(id, f"Не понимаю")


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
