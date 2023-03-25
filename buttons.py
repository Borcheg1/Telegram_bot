from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

btn_yes = KeyboardButton('Да ✅')
btn_no = KeyboardButton('Нет ❌')

btn_change_yes = KeyboardButton('Изменить данные ✍')
btn_change_no = KeyboardButton('Оставить без изменений ✋')

btn_reg = KeyboardButton('Регистрация 🎓')
btn_quiz = KeyboardButton('Викторина 🎮')
btn_prices = KeyboardButton('Цены 💰')
btn_delete = KeyboardButton('Удаление ⛔')

btn_quiz_start = KeyboardButton('Начать ✅')
btn_quiz_cancel = KeyboardButton('Отменить ❌')


verification_keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
verification_keyboard.add(btn_yes, btn_no)

change_reg_keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
change_reg_keyboard.add(btn_change_yes, btn_change_no)

menu_keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
menu_keyboard.add(btn_reg, btn_quiz, btn_prices)

quiz_keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
quiz_keyboard.add(btn_quiz_start, btn_quiz_cancel)
