from aiogram.types import KeyboardButton,ReplyKeyboardMarkup,InlineKeyboardButton,InlineKeyboardMarkup,KeyboardButtonRequestUser

keyboards = KeyboardButtonRequestUser(request_id=1, user_is_bot=False, user_is_premium=False)
button = KeyboardButton(text="Выбрать пользователя", request_user=keyboards)


start_mes = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='Поиск по номеру 📱'),KeyboardButton(text='🔎 Поиск по IP')],
    [KeyboardButton(text='💼 Простой Ddos'),KeyboardButton(text='🕵️ ️Мой профиль')],
    [button,KeyboardButton(text='📊 Статистика')],
],



  resize_keyboard=True,
  input_field_placeholder='Выберите пункт меню...'

)
json_user = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Json',callback_data='json')]
])

sub_check = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Канал',url='https://t.me/development_progs')]
])
