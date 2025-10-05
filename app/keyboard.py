from aiogram.types import KeyboardButton,ReplyKeyboardMarkup,InlineKeyboardButton,InlineKeyboardMarkup,KeyboardButtonRequestUser

keyboards = KeyboardButtonRequestUser(request_id=1, user_is_bot=False, user_is_premium=False)
button = KeyboardButton(text="Выбрать пользователя", request_user=keyboards)


start_mes = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='Поиск по номеру 📱'),KeyboardButton(text='🔎 Поиск по IP')],
    [KeyboardButton(text='💼 Простой Ddos'),KeyboardButton(text='📧 E-mail')],
    [button,KeyboardButton(text='📖 Меню')],
],


  resize_keyboard=True,
  input_field_placeholder='Выберите пункт меню...'

)

menu_mes = ReplyKeyboardMarkup(keyboard=[
  [KeyboardButton(text='📊 Статистика'),KeyboardButton(text='💰 Пополнить')],
  [KeyboardButton(text='🕵️ ️Мой профиль'),KeyboardButton(text='👤 Аккаунт')]

],
  resize_keyboard=True
)
ip_get = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Узнать IP',url='https://www.securitylab.ru/blog/personal/simlpehacker/353024.php?ysclid=mfy6vuxnui598178234&utm_referrer=https%3A%2F%2Fyandex.by%2F')]
])
json_user = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Json',callback_data='json')]
])

sub_check = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Канал',url='https://t.me/development_progs')]
])
