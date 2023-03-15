from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

btn_yes = KeyboardButton('Да ✅')
btn_no = KeyboardButton('Нет ❌')

verification_keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
verification_keyboard.add(btn_yes, btn_no)
