import asyncio
import requests

from faker import Faker
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram import F,Router,Bot

import random
from config import ADMIN_ID, TOKEN
from database import SessionLocal,User,BroadCast

from aiogram.enums import ChatMemberStatus
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, UserShared
from aiogram.enums import ContentType
from aiogram.types import CallbackQuery,Message
from aiogram.filters import CommandStart,Command
from aiogram.fsm.state import State,StatesGroup
from aiogram.fsm.context import FSMContext

from app.keyboard import start_mes,json_user,sub_check
from geopy import Nominatim
import phonenumbers
from phonenumbers import timezone,geocoder,carrier,is_possible_number


router = Router()
bot = Bot(token=TOKEN)
fake = Faker()



CHANEl_ID = '-1002939673303'
ADMIN_ID = ADMIN_ID




class Ip(StatesGroup):
      ip_adress = State()

class TeleOsint(StatesGroup):
      telephone = State()

class Ddoss(StatesGroup):
      target = State()
      number = State()

class BroadcastState(StatesGroup):
    wait_text = State()


async def  check_member(chat_member,message:Message):
    try:
        chat_member = await bot.get_chat_member(chat_id=CHANEl_ID,user_id=message.from_user.id)
        print(chat_member.status)
        if  chat_member.status == ChatMemberStatus.LEFT:
            return False
        else:
            return True
    except Exception as e:
        print(f"Ошибка в {e} ")



def admin_main_menu():
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📊‍Статистика",callback_data='stats')],
        [InlineKeyboardButton(text='✉️Рассылка',callback_data='broadcast')],
        [InlineKeyboardButton(text='⚙️Доп настройки',callback_data='settings')]
    ])
    return keyboard
def back_menu():
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='Back',callback_data='back')],
    ])
    return keyboard


@router.message(Command("admin"))
async def admin_panel(message:Message):
   if message.from_user.id != ADMIN_ID:
       await message.answer('У вас нет доступа к этой команде.')
       return
   await message.answer("Добро пожаловать в админ панель бота 🌍❤️❤️!",reply_markup=admin_main_menu())
@router.callback_query(F.data == 'back')
async def back_menu(callback:CallbackQuery):
    await callback.message.answer("",reply_markup=admin_main_menu())
    await callback.answer('')

@router.callback_query(F.data == 'stats')
async def stats_process(callback:CallbackQuery):
    db = SessionLocal()
    total_users = db.query(User).count()
    active_users = db.query(User).filter(User.active == True).count()
    db.close()
    text = f'Статистика:\nВсего пользователей 🕵️: {total_users}\nАктивных пользователей 🎮: {active_users}'
    await callback.message.answer(f'{text}')
    await callback.answer('')
@router.callback_query(F.data == 'broadcast')
async def broadcast_start(callback:CallbackQuery,state:FSMContext):
    await callback.message.answer("Введите текст для рассылки ✉️")
    await state.set_state(BroadcastState.wait_text)
    await callback.answer('')
@router.callback_query(F.data == 'settings')
async def settings(callback:CallbackQuery):
    await callback.message.answer("Я рома тик так ")
    await callback.answer('')

@router.message(BroadcastState.wait_text)
async def broadcast_mess(message:Message,state:FSMContext,bot:Bot):
    broadcast_text = message.text
    db = SessionLocal()
    users_list = db.query(User).filter(User.active == True).all()
    count = 0
    for user in users_list:
        try:
            await bot.send_message(user.telegram_id,broadcast_text)
            count +=1
        except Exception as e:
            print(f'Failed to send to {user.telegram_id}:{e}')
    new_broadcast = BroadCast(message=broadcast_text)
    db.add(new_broadcast)
    db.commit()
    db.close()
    await message.answer(f"Рассылка завершена ✉️ ! Сообщение отправлено {count} пользователям 🕵️.",reply_markup=start_mes)
    await state.clear()

@router.message(CommandStart())
async def start(message:Message):
    if await check_member(CHANEl_ID,message):

       db = SessionLocal()
       exiting = db.query(User).filter(User.telegram_id == message.from_user.id).first()
       if not exiting:
           new_user = User(telegram_id=message.from_user.id,name=message.from_user.full_name)
           db.add(new_user)
           db.commit()
       db.close()

       await message.answer_photo(photo='https://avatars.mds.yandex.net/i?id=769d260e9f9b31f55a982b64733f53ce-4902121-images-thumbs&n=13',caption=f"Привет {message.from_user.full_name} я бот  🔎 для <b>Osint</b>💻\nпробива,поиска пользователей тг .\nВы подписаны на уведомления всегда  📫 !\nУдачи тебе пробить жертву.\n\n",parse_mode='HTML',reply_markup=start_mes)
    else:
        await message.answer("🌍 Подпишитесь на канал",reply_markup=sub_check)


@router.message(F.content_type == ContentType.USERS_SHARED)
async def search(message:Message):
    bot_message = await message.answer("🔎Идет поиск информации...")
    usera = message.user_shared

    message_id_user = usera.user_id

    phone_user = usera.json()
    shares = f'tg://openmessage?user_id={usera.user_id}'
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='Telegram',url=shares)],


    ])



    await asyncio.sleep(1)

    await message.reply(f'Ваш пользователь пробит:\n\n├📝 Id: {message_id_user}\n├💭 Ссылка:{shares}\n\n└ Info: {phone_user}\n',reply_markup=keyboard)

    await asyncio.sleep(2)
    await message.answer("🤖Поиск завершен",reply_markup=start_mes)

@router.message(F.text == '📊 Статистика')
async def stats(message:Message):
    db = SessionLocal()
    total_users = db.query(User).count()
    active_users = db.query(User).filter(User.active == True).count()
    db.close()
    text = f'📊 Статистика:\n\n├ Всего 👀 пользователей: {total_users}\n├ Активных 🎮 пользователей : {active_users}\n└ Реферальная ссылка 📎 : t.me/phone_osint_up_bot'
    await message.answer(f'{text}',reply_markup=start_mes)
@router.message(F.content_type == ContentType.CONTACT)
async def contact_share(message:Message):
    if await check_member(CHANEl_ID, message):
       await message.answer('Идет поиск 🔎 информации...')
       await asyncio.sleep(1.5)
       contact = message.contact
       vcard = contact.vcard

       # Извлекаем данные
       phone_number = contact.phone_number
       first_name = contact.first_name
       last_name = contact.last_name if contact.last_name else ""
       user_id = contact.user_id
       name_json= contact.json()

       tg_phone = f'https://t.me/{phone_number}'
       wt_phone = f'https://wa.me/{phone_number}'

       keyboards_start = InlineKeyboardMarkup(inline_keyboard=[[
           InlineKeyboardButton(text='Telegram', url=tg_phone),
           InlineKeyboardButton(text='WhatsApp', url=wt_phone)
       ]])

       response = f"""
       📞 Получен контакт:
       ├ Номер: {phone_number}
       ├ Имя: {first_name}
       ├ Фамилия: {last_name}
       ├ ID пользователя: {user_id}
       ├ Json: {name_json}
       └ vCard: {vcard}
     
        """
       await message.answer(f'{response}',reply_markup=keyboards_start)

@router.message(F.text == 'Поиск по номеру 📱')
async def tele_osint(message:Message,state:FSMContext):
    await state.set_state(TeleOsint.telephone)
    await message.answer('Введи номер мобильного 📱 телефона жертвы 😭🥷. ')

@router.message(TeleOsint.telephone)
async def tele_infa(message:Message,state:FSMContext):
    bot_message = await message.answer("Идет поиск 🔎 информации...")
    await state.update_data(telephone = message.text)

    phone = message.text
    phone_valid = phone.replace(' ', '')
    if not int(phone):
        await message.answer("Введите корректный номер телефона📱")
        await state.clear()
    elif len(phone_valid) < 10:
        await message.answer('🤖 Введите корректный номер телефона📱')
        await state.clear()
    else:
       num_dump = random.randint(0,6)
       phone_number = phonenumbers.parse(phone)
       possible = phonenumbers.is_possible_number(phone_number)
       carrier1 = carrier.name_for_number(phone_number, 'ru')

       geocoder1 = geocoder.description_for_number(phone_number, "ru")
       timezone1 = timezone.time_zones_for_number(phone_number)
       valid = phonenumbers.is_valid_number(phone_number)



       if valid == True:
           valid = 'Да'
       else:
           valid = 'Нет'
       await asyncio.sleep(2)

       guest_phone_number = phone_valid
       tg_id = f'https://tg-user.id/from/username/'


       tg_chat = f'https://t.me/{phone_valid}'


       keyboard = InlineKeyboardMarkup(inline_keyboard=[
           [InlineKeyboardButton(text='Telegram',url=tg_chat),InlineKeyboardButton(text='Сайт',url=tg_id)],
           [InlineKeyboardButton(text='WhatsApp',url=f'https://wa.me/{phone_valid}')]

       ])

       if num_dump == 0:
           text_email = 'Ничего не найдено'
       elif num_dump == 1:
            text_email = fake.email()

       elif num_dump == 2:
           first_txt = fake.email()
           second_txt = fake.email()
           text_email = first_txt,second_txt

       elif num_dump == 3:
           first_txt = fake.email()
           second_txt = fake.email()
           third_txt = fake.email()
           text_email = first_txt, second_txt,third_txt

       elif num_dump == 4:
           first_txt = fake.email()
           second_txt = fake.email()
           third_txt = fake.email()
           four_txt = fake.email()
           text_email = first_txt, second_txt, third_txt,four_txt

       elif num_dump == 5:
           first_txt = fake.email()
           second_txt = fake.email()
           third_txt = fake.email()
           four_txt = fake.email()
           firth_txt = fake.email()
           text_email = first_txt, second_txt, third_txt,four_txt,firth_txt

       elif num_dump == 6:
           first_txt = fake.email()
           second_txt = fake.email()
           third_txt = fake.email()
           four_txt = fake.email()
           firth_txt = fake.email()
           six_txt = fake.email()
           text_email = first_txt, second_txt, third_txt,four_txt,firth_txt,six_txt


       text_osint = f'Поиск  ️🤖💻📱 прошел успешно:\n\n├ Телефон: {phone}\n├ Оператор: {carrier1}\n├ Регион: {timezone1}\n├ Страна: {geocoder1}\n├ Валид: {valid}\n└ Существует: {possible}\n\n📧 E-mail: {text_email}\n📝Телефонные книги: None\n\nСсылка: {tg_chat}'

       await bot_message.reply(text_osint,reply_markup=keyboard)

    await asyncio.sleep(1)
    await message.answer('Поиск закончился все данные вверху.',reply_markup=start_mes)

    await state.clear()


@router.message(F.text == '🔎 Поиск по IP')
async def ip_osint(message:Message,state:FSMContext):
    await state.set_state(Ip.ip_adress)
    await message.answer('Введите Ip адресс жертвы')

@router.message(Ip.ip_adress)
async def ip_search(message:Message,state:FSMContext):
    bot_message = await message.answer('Идет поиск 🔎 информации...')
    await state.update_data(ip_adress=message.text)
    ip = message.text
    try:
        response = requests.get(url=f'http://ip-api.com/json/{ip}').json()



        text = f"Поиск  ️🤖💻📱 прошел успешно:\n\nIP: {ip}\n├ Провайдер: {response.get('isp')}\n├ Организация: {response.get('org')}\n├ Ofset: {response.get('offset')}\n├ Валюта: {response.get('BYR')}\n├ As: {response.get('as')}\n├ As_name: {response.get('asname')}\n├ Мобильный ip:{response.get('mobile')}\n├ Прокси: {response.get('proxy')}\n├ Hosting: {response.get('hosting')}\n├ DNS:{response.get('dns')}\n├ Континент: {response.get('continentCode')}\n├ Страна: {response.get('country')}\n├ Регион: {response.get('regionName')}\n├ Город: {response.get('city')}\n├ ZIP: {response.get('zip')}\n├ Широта: {response.get('lat')}\n└ Долгота: {response.get('lon')}"

        await bot_message.edit_text(text)
        await asyncio.sleep(2)
        coordinates = f"{response.get('lat')},{response.get('lon')}"
        nominaltim = Nominatim(user_agent='user')
        location = nominaltim.reverse(coordinates)



        await message.answer_location(latitude=response.get('lat'),longitude=response.get('lon'))
        await message.answer(f'-- Поиск по координатам 🌍:\n\n{str(location)}', reply_markup=start_mes)

    except requests.exceptions.ConnectionError:
        await message.answer('Увы информация не найдена')
    await state.clear()

@router.message(F.text == '💼 Простой Ddos')
async def ddos_start(message:Message,state:FSMContext):
    await state.set_state(Ddoss.target)
    await message.answer("Введите URL 🔎 жертвы 🌍💻 ")

@router.message(Ddoss.target)
async def ddos(message:Message,state:FSMContext):

    await state.update_data(target=message.text)
    await state.set_state(Ddoss.number)

    await message.answer('Введи количество пакетов🛍️ не больше 100')

@router.message(Ddoss.number)
async def ddosing(message:Message,state:FSMContext):
    await state.update_data(number = message.text)
    data = await state.get_data()
    target = data['target']

    sockets = int(message.text)
    print(target,sockets)
    if sockets >= 100:
       sockets = 10
    else:
        sockets = sockets

    for num in range(sockets):
        soket = requests.get(target)
        if soket.status_code == 200:
            await message.answer(f'Пакет🛍️ отправлен')
        else:
             await message.answer(f'Пакет не отправлен')
    await asyncio.sleep(1)
    await message.answer('Dos атака ⚔️🛍️💻 закончилась все данные вверху.',reply_markup=start_mes)
    await state.clear()

@router.message(F.text == '🕵️ ️Мой профиль')
async def profile(message:Message):
    db = SessionLocal()

    user = db.query(User).filter(User.telegram_id == id).first()
      
    db.close()
    prem = message.from_user.is_premium
    if prem == None:
       prem = "Нету"
    else:
        prem = 'Есть'

    await message.reply(f'Мой профиль🧰:\n\n├ Имя: {message.from_user.full_name}\n├ Username: @{message.from_user.username}\n├ Telegram_Id: {message.from_user.id}\n├ Регистрация:{user.register_at}\n├ Баланс: 0$\n├ Премиум: {prem}\n└ Язык: {message.from_user.language_code}',reply_markup=json_user)

@router.callback_query(F.data =='json')
async def json(callback:CallbackQuery):
    jsons = callback.from_user.json()
    await callback.answer('')
    await callback.message.answer(f"{jsons}")

@router.message(F.text[0] == "@")
async def text_start(message: Message):
    if await check_member(CHANEl_ID, message):
        username = message.text
        user_first = username.replace("@", "")
        first_letter = username[0]

        if first_letter == '@':

            await message.answer('Идет поиск 🔎 информации...')
            url = f'https://tg-user.id/from/username/{user_first}'
            keyboard = InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text='Узнать', url=url)],
                [
                    InlineKeyboardButton(
                        text='Telegram',
                        url=f'https://telegram.me/{user_first}')
                ]
            ])
            await message.answer(
                f"Пользователь найден:\nUsername : {username}",
                reply_markup=keyboard)

        else:
            await message.answer('Введи корректое имя.')
    else:
        await message.answer("🌍Подпишитесь на канал", reply_markup=sub_check)




