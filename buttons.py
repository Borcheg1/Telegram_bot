from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

# Создание кнопок.
btn_yes = KeyboardButton('Да ✅')
btn_no = KeyboardButton('Нет ❌')

btn_change_yes = KeyboardButton('Изменить данные ✍')
btn_change_no = KeyboardButton('Оставить без изменений ✋')

btn_reg = KeyboardButton('Регистрация 🎓')
btn_quiz = KeyboardButton('Викторина 🎮')
btn_prices = KeyboardButton('Цены 💰')
btn_delete = KeyboardButton('Удаление ⛔')

btn_start = KeyboardButton('/start')


# Cоздание клавиатуры с кнопками 'Да ✅', 'Нет ❌'. Клавиатура одноразовая.
yes_no_keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
yes_no_keyboard.add(btn_yes, btn_no)

# Cоздание клавиатуры с кнопками 'Изменить данные ✍', 'Оставить без изменений ✋'. Клавиатура одноразовая.
change_reg_keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
change_reg_keyboard.add(btn_change_yes, btn_change_no)

# Cоздание клавиатуры с кнопками 'Регистрация 🎓', 'Викторина 🎮', 'Цены 💰', 'Удаление ⛔'.
menu_keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
menu_keyboard.add(btn_reg, btn_quiz, btn_prices, btn_delete)

# Создание клавиатуры с кнопкой '/start'.
start_keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
start_keyboard.add(btn_start)
