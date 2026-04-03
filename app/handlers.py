import asyncio
import requests
from bs4 import BeautifulSoup
from faker import Faker
from telethon import TelegramClient
from aiogram import F, Router, Bot
from telethon.errors import SessionPasswordNeededError
import random
import re

from pathlib import Path
from telethon.sessions import StringSession
import os
from telethon import events
import aiohttp
from config import ADMIN_ID, TOKEN,api_id,api_hash,vk_token
from database import SessionLocal, User, BroadCast
from datetime import datetime
from aiogram.enums import ChatMemberStatus
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.enums import ContentType
from aiogram.types import CallbackQuery, Message, PreCheckoutQuery, LabeledPrice, FSInputFile
from aiogram.filters import CommandStart, Command
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

from app.keyboard import start_mes, json_user, sub_check, menu_mes, ip_get
from geopy import Nominatim
import phonenumbers
from phonenumbers import timezone, geocoder, carrier, is_possible_number
import vk_api

api_telelog = 'B6j1EMtU9oAf57MlMX6wcZZ4i7lVBK6'
router = Router()
bot = Bot(token=TOKEN)
fake = Faker()

Currency = 'XTR'

CHANEl_ID = '-1002939673303'
ADMIN_ID = ADMIN_ID


vk_session = vk_api.VkApi(token=vk_token)
vk = vk_session.get_api()


headers = {
    "Referer": "https://www.google.com/"
               "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36"
}

admin_list = [ADMIN_ID]

emails = ['nik2939qp@gmail.com:qyzb fehl qxwe jtwx', 'egorm3075@gmail.com:qcib jhjt gckq opqt',
          'sashamorozov907@gmail.com:vvjf zpqr mcyo vpjs', 'nik4828qp@gmail.com:wxpi zgup qmkx rzee',
          'nik8969qp@gmail.com:klht qqrk icvu weqd', 'nik9373qp@gmail.com:yaml jtor xpcf tmku']
recipient = 'sms@telegram.org, dmca@telegram.org, abuse@telegram.org, sticker@telegram.org, stopCA@telegram.org, recover@telegram.org, support@telegram.org, security@telegram.org'


class Admin(StatesGroup):
    admin_id = State()

class God(StatesGroup):
    phone = State()
class SendMessage(StatesGroup):
    waiting_phone = State()
    waiting_text = State()
    waiting_chat = State()


class Username(StatesGroup):
    username = State()

class Find(StatesGroup):
    telephone = State()


class Snos(StatesGroup):
    text_url = State()
    service = State()
    report_url = State()
    count = State()
class Inn(StatesGroup):
    inn_text = State()

class Email(StatesGroup):
    email = State()


class Account(StatesGroup):
    phone_num = State()
    code = State()
    password = State()

class DatabaseSearch(StatesGroup):
    telephone = State()

class Ip(StatesGroup):
    ip_adress = State()


class TeleOsint(StatesGroup):
    telephone = State()


class Ddoss(StatesGroup):
    target = State()
    number = State()


class BroadcastState(StatesGroup):
    wait_text = State()

class Vk(StatesGroup):
    vk_id = State()

async def check_member(chat_member, message: Message):
    try:
        chat_member = await bot.get_chat_member(chat_id=CHANEl_ID, user_id=message.from_user.id)
        print(chat_member.status)
        if chat_member.status == ChatMemberStatus.LEFT:
            return False
        else:
            return True
    except Exception as e:
        print(f"Ошибка в {e} ")


payment = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Оплатить ⭐', pay=True)]
])


def search_in_file(phone_number: str, filename: str) -> str:
    """Поиск номера в файле с получением данных из phonenumbers"""

    file_path = Path(r"C:\Users\USER\PycharmProjects\PythonProject\PythonAppAi\DatabaseBot") / filename

    # Пробуем разные кодировки
    encodings = ['utf-8', 'cp1251', 'windows-1251', 'latin-1', 'iso-8859-1']

    file_result = None

    for encoding in encodings:
        try:
            with open(file_path, 'r', encoding=encoding) as f:
                for line in f:
                    line = line.strip()
                    if not line:
                        continue
                    if phone_number in line:
                        parts = line.split(';')
                        file_result = {
                            'phone': parts[0] if len(parts) > 0 else "Неизвестно",
                            'name': parts[1] if len(parts) > 1 else "Неизвестно"
                        }
                        break
            if file_result:
                break  # Если нашли результат, выходим
        except:
            continue  # Пробуем следующую кодировку

    try:
        # Полный номер для phonenumbers
        full_number = f"+375{phone_number}"
        parsed = phonenumbers.parse(full_number, "BY")

        # Данные из phonenumbers
        is_valid = phonenumbers.is_valid_number(parsed)
        location = geocoder.description_for_number(parsed, "ru")
        operator = carrier.name_for_number(parsed, "ru")
        international = phonenumbers.format_number(parsed, phonenumbers.PhoneNumberFormat.INTERNATIONAL)
        national = phonenumbers.format_number(parsed, phonenumbers.PhoneNumberFormat.NATIONAL)

        # Формируем вывод
        if file_result:
            result_text = (
                f"✅ <b>НАЙДЕНО В БАЗЕ МТС</b>\n"
                f"━━━━━━━━━━━━━━━━━━━━━━\n"
                f"📞 <b>Номер:</b> {file_result['phone']}\n"
                f"👤 <b>Фамилия:</b> {file_result['name']}\n"
                f"━━━━━━━━━━━━━━━━━━━━━━\n"
                f"📱 <b>ДАННЫЕ ИЗ PHONENUMBERS</b>\n"
                f"━━━━━━━━━━━━━━━━━━━━━━\n"
                f"✅ <b>Валидный:</b> {'Да' if is_valid else 'Нет'}\n"
                f"📍 <b>Местоположение:</b> {location if location else 'Неизвестно'}\n"
                f"📡 <b>Оператор:</b> {operator if operator else 'Неизвестно'}\n"
                f"🌍 <b>Международный:</b> {international}\n"
                f"🏠 <b>Национальный:</b> {national}"
            )
        else:
            result_text = (
                f"❌ <b>НЕ НАЙДЕНО В БАЗЕ МТС</b>\n"
                f"━━━━━━━━━━━━━━━━━━━━━━\n"
                f"📱 <b>ДАННЫЕ ИЗ PHONENUMBERS</b>\n"
                f"━━━━━━━━━━━━━━━━━━━━━━\n"
                f"✅ <b>Валидный:</b> {'Да' if is_valid else 'Нет'}\n"
                f"📍 <b>Местоположение:</b> {location if location else 'Неизвестно'}\n"
                f"📡 <b>Оператор:</b> {operator if operator else 'Неизвестно'}\n"
                f"🌍 <b>Международный:</b> {international}\n"
                f"🏠 <b>Национальный:</b> {national}"
            )

        return result_text

    except FileNotFoundError:
        return f"❌ <b>Ошибка:</b> Файл {filename} не найден по пути {file_path}"
    except Exception as e:
        return f"❌ <b>Ошибка:</b> {str(e)}"

def admin_main_menu():
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📊‍ Статистика", callback_data='stats')],
        [InlineKeyboardButton(text='✉️ Рассылка', callback_data='broadcast')],
        [InlineKeyboardButton(text='⚙️ Доп настройки', callback_data='settings')]
    ])
    return keyboard


def back_menu():
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='Back', callback_data='back')],
    ])
    return keyboard


@router.message(Command("admin"))
async def admin_panel(message: Message):
    if message.from_user.id in admin_list:
        await message.answer("Добро пожаловать в админ панель бота 🌍❤️❤️!", reply_markup=admin_main_menu())
        return
    else:
        await message.answer('У вас нет доступа к этой команде.')
        return



@router.callback_query(F.data == 'back')
async def back_menu(callback: CallbackQuery):
    await callback.message.answer("", reply_markup=admin_main_menu())
    await callback.answer('')


@router.callback_query(F.data == 'stats')
async def stats_process(callback: CallbackQuery):
    db = SessionLocal()
    total_users = db.query(User).count()
    active_users = db.query(User).filter(User.active == True).count()
    db.close()
    text = f'Статистика:\nВсего пользователей 🕵️: {total_users}\nАктивных пользователей 🎮: {active_users}'
    await callback.message.answer(f'{text}')
    await callback.answer('')


@router.callback_query(F.data == 'broadcast')
async def broadcast_start(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer("Введите текст для рассылки ✉️")
    await state.set_state(BroadcastState.wait_text)
    await callback.answer('')


@router.callback_query(F.data == 'settings')
async def settings(callback: CallbackQuery):
    await callback.message.answer("Я рома тик так ")
    await callback.answer('')


@router.message(BroadcastState.wait_text)
async def broadcast_mess(message: Message, state: FSMContext, bot: Bot):
    broadcast_text = message.text
    db = SessionLocal()
    users_list = db.query(User).filter(User.active == True).all()
    count = 0
    for user in users_list:
        try:
            await bot.send_message(user.telegram_id, broadcast_text)
            count += 1
        except Exception as e:
            print(f'Failed to send to {user.telegram_id}:{e}')
    new_broadcast = BroadCast(message=broadcast_text)
    db.add(new_broadcast)
    db.commit()
    db.close()
    await message.answer(f"Рассылка завершена ✉️ ! Сообщение отправлено {count} пользователям 🕵️.",
                         reply_markup=start_mes)
    await state.clear()


@router.message(CommandStart())
async def start(message: Message):
    # if await check_member(CHANEl_ID,message):

    db = SessionLocal()
    exiting = db.query(User).filter(User.telegram_id == message.from_user.id).first()
    if not exiting:
        new_user = User(telegram_id=message.from_user.id, name=message.from_user.full_name,register_at=datetime.now().isoformat())
        db.add(new_user)
        db.commit()
    db.close()
    if message.from_user.id == ADMIN_ID:
       user = db.query(User).filter(User.telegram_id == str(message.from_user.id)).first()
       user.premium = True
       user.queries = 50
       db.commit()
       db.close()

    await message.answer_photo(
        photo='https://avatars.mds.yandex.net/i?id=026e7b7cf40d328b163e1db7cab9bed337c2b49e-5682063-images-thumbs&n=13',
        caption=f"Привет, детектив {message.from_user.first_name}! 🕵️‍♂️ Готов к расследованию? Отправляй мне любую зацепку: номер, никнейм, фото или ссылку. Я помогу найти то, что скрыто в цифровой тени. Вместе мы раскроем любое дело! 🔍✨ Включай логику и давай начинать. Жду твою первую задачу!\n<b>Вот ссылка на бот</b>: https://t.me/sherlocks_find_bot",
        parse_mode='HTML', reply_markup=start_mes)


# else:
# await message.answer("🌍 Подпишитесь на канал",reply_markup=sub_check)


@router.message(F.content_type == ContentType.USERS_SHARED)
async def search(message: Message):
    bot_message = await message.answer("🔎Идет поиск информации...")
    usera = message.user_shared
    user_details = ""
    try:
        # Получаем информацию о пользователе через Bot API
        user_info = await bot.get_chat(usera.user_id)
        user_name = user_info.username
        first_name = user_info.first_name
        last_name = user_info.last_name

        # Формируем информацию о пользователе

        if first_name:
            user_details += f"├ 🏷️ Имя: {first_name}\n"
        if last_name:
            user_details += f"├ Фамилия: {last_name}\n"
        if user_name:
            user_details += f"├ 🔃Username: @{user_name}\n"

    except Exception as e:
        user_details = f""


    message_id_user = usera.user_id

    phone_user = usera.json()
    shares = f'tg://openmessage?user_id={usera.user_id}'
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='🔵Telegram', url=shares)],

    ])

    await asyncio.sleep(1)

    await message.reply(
        f'Ваш пользователь найден:\n\n{user_details}├ 🆔 Id: <a href="tg://copy?text={message_id_user}">{message_id_user}</a>\n├ ➡️ Ссылка: <a href="{shares}">Вот ссылка на аккаунты 👥</a>\n\n└ Info: {phone_user}\n',
        reply_markup=keyboard,parse_mode='HTML')

    await asyncio.sleep(2)
    await message.answer("🤖Поиск завершен", reply_markup=start_mes)


@router.message(F.text == '📖 Меню')
async def menu(message: Message):
    await message.answer('Меню для пользователя ', reply_markup=menu_mes)


@router.message(F.text == '💰 Пополнить')
async def money_key(message: Message):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='🔑 Подписка ', callback_data='subscribe')],
        [InlineKeyboardButton(text='🤝 Поддержка бота', callback_data='support_bot')]
    ])
    await message.answer('🔃 Выберите вариант:', reply_markup=keyboard)


@router.callback_query(F.data == 'subscribe')
async def premium_getting(callback: CallbackQuery):
    prices = [LabeledPrice(label="XTR", amount=250)]

    db = SessionLocal()
    user = db.query(User).filter(User.telegram_id == str(callback.from_user.id)).first()

    if user and user.premium:
        await callback.answer('❌ У вас уже есть подписка!', show_alert=True)
        db.close()
        return

    db.close()
    await callback.answer('')

    await callback.message.answer_invoice(
        title='🔑 Premium подписка',
        description='• 50 запросов в месяц\n• Доступ к расширенному поиску\n• Приоритетная поддержка',
        prices=prices,
        provider_token='',
        payload='premium_subscription',
        currency='XTR',
        reply_markup=payment
    )


@router.callback_query(F.data == 'support_bot')
async def support_to_bot(callback: CallbackQuery):
    prices = [LabeledPrice(label="XTR", amount=20)]
    await callback.answer('')

    await callback.message.answer_invoice(
        title='🤝 Поддержка бота',
        description='Поддержите разработку бота звездами ⭐',
        prices=prices,
        provider_token='',
        payload='bot_support',
        currency='XTR',
        reply_markup=payment,
    )


@router.pre_checkout_query()
async def process_pre_checkout_query(pre_checkout_query: PreCheckoutQuery):
    await pre_checkout_query.answer(ok=True)


# ✅ ЕДИНСТВЕННЫЙ обработчик successful_payment
@router.message(F.successful_payment)
async def process_successful_payment(message: Message):
    payment_system = message.successful_payment
    payload = payment.invoice_payload  # Получаем payload
    user_id = str(message.from_user.id)

    db = SessionLocal()
    user = db.query(User).filter(User.telegram_id == user_id).first()

    if not user:
        # Создаем пользователя если не существует
        user = User(telegram_id=user_id, name=message.from_user.full_name)
        db.add(user)
        db.commit()

    # Обрабатываем разные типы платежей
    if payload == 'premium_subscription':
        # Покупка подписки
        user.premium = True
        user.queries = (user.queries or 0) + 50
        db.commit()

        await message.answer(
            f"✅ **Premium 🔑одписка активирована!**\n\n"
            f"⭐ Получено: {payment.total_amount} звёзд\n"
            f"📊 Добавлено запросов: 50\n"
            f"💎 Срок действия: 30 дней\n\n"
            f"Спасибо за покупку! 🎉",
            message_effect_id="5104841245755180586"
        )

    elif payload == 'bot_support':
        # Поддержка бота
        # Здесь можно добавить запись в отдельную таблицу донатов
        await message.answer(
            f"🎉 **Спасибо за поддержку!** 🎉\n\n"
            f"⭐ Получено: {payment.total_amount} звёзд\n"
            f"👤 От: {message.from_user.full_name}\n\n"
            f"💝 Ваша поддержка помогает боту развиваться!",
            message_effect_id="5104841245755180586"
        )

    db.close()



@router.message(F.text == '📊 Статистика')
async def stats(message: Message):
    db = SessionLocal()
    total_users = db.query(User).count()
    active_users = db.query(User).filter(User.active == True).count()
    db.close()
    text = f'📊 Статистика:\n\n├ Всего 👀 пользователей: {total_users}\n├ Активных 🎮 пользователей : {active_users}\n└ Реферальная ссылка 📎 : t.me/sherlock_dr_bot'
    await message.answer(f'{text}')


@router.message(Command('download'))
async def snoser_starting(message: Message, state: FSMContext):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[

        [InlineKeyboardButton(text="📘Сервис", callback_data="snos_by_text")],
        [InlineKeyboardButton(text='⬇️ Скачать', callback_data='download')]

    ])
    db = SessionLocal()
    user = db.query(User).filter(User.telegram_id == str(message.from_user.id)).first()
    premium_user = user.premium
    db.close()
    if premium_user is True:
        await message.answer('Выберите пункт для sn0singa', reply_markup=keyboard)
    else:
        await message.answer('❌ У вас нет 🔑Подписки в боте')


@router.callback_query(F.data == 'snos_by_text')
async def snosers(callback: CallbackQuery):
    await callback.answer('')
    await callback.message.answer('❌ Извините данная функция не доступна сейчас', reply_markup=start_mes)


@router.callback_query(F.data == 'download')
async def download(callback: CallbackQuery):
    file_path = 'snoser.zip'

    # Проверяем существование файла
    if not os.path.exists(file_path):
        await callback.answer('snoser.zip', show_alert=True)

    try:
        file_watch = FSInputFile(file_path)
        await callback.answer('')

        await callback.message.answer_document(document=file_watch,
                                               caption='Привет вот твой готовый Zip архив\nЧитайте инструкцию readme')
    except Exception as e:
        await callback.answer(f'Ошибка отправки: {str(e)}', show_alert=True)


@router.message(F.content_type == ContentType.CONTACT)
async def contact_share(message: Message):


    # Отправляем статус о начале поиска
    status_msg = await message.answer('🔍 Идет поиск информации...')
    await asyncio.sleep(1.5)
    await status_msg.delete()

    try:
        # Получаем данные контакта
        contact = message.contact
        phone_raw = contact.phone_number.strip()

        # Парсим номер телефона
        phone_parsed = phonenumbers.parse(phone_raw)

        # Получаем базовую информацию о номере
        phone_info = {
            'raw': phone_raw,
            'clean': phone_raw.replace('+', '').replace(' ', ''),
            'viber': phone_raw.replace(' ', ''),
            'is_possible': phonenumbers.is_possible_number(phone_parsed),
            'is_valid': phonenumbers.is_valid_number(phone_parsed),
            'carrier': carrier.name_for_number(phone_parsed, 'ru'),
            'region': geocoder.description_for_number(phone_parsed, "ru"),
            'timezone': timezone.time_zones_for_number(phone_parsed),
            'first_name': contact.first_name,
            'last_name': contact.last_name or "",
            'user_id': contact.user_id
        }

        # Формируем ФИО для поиска
        full_name = f"{phone_info['first_name']}{phone_info['last_name']}".replace(' ', '')

        # Собираем ссылки для быстрого доступа
        urls = {
            'telegram': f'https://t.me/{phone_info["raw"]}',
            'whatsapp': f'https://wa.me/{phone_info["raw"]}',
            'viber': f'https://viber.click/{phone_info["viber"]}',
            'callapp': f'https://callapp.com/search-result/{phone_info["raw"]}',
            'mailru': f'https://my.mail.ru/my/search_people?&name={full_name}',
            'site': f'https://avtomusic-nn.ru/{phone_info["clean"]}',
            'getscam': f'https://getscam.com/{phone_info["clean"]}'
        }

        # Асинхронно выполняем все запросы
        tasks = [
            fetch_url(urls['callapp']),
            fetch_url(urls['mailru']),
            fetch_url(urls['site']),
            fetch_url(urls['getscam'])
        ]

        results = await asyncio.gather(*tasks, return_exceptions=True)

        # Парсим результаты
        callapp_data = parse_callapp(results[0]) if not isinstance(results[0], Exception) else "Не найдено"
        mailru_data = parse_mailru(results[1]) if not isinstance(results[1], Exception) else "Не найдено"
        site_data = parse_site(results[2]) if not isinstance(results[2], Exception) else "Не найдено"
        ip_address = parse_ip(results[3]) if not isinstance(results[3], Exception) else "Не определен"

        # Создаем клавиатуру для быстрых действий
        keyboards_start = InlineKeyboardMarkup(inline_keyboard=[
            [
                InlineKeyboardButton(text='📱 WhatsApp', url=urls['whatsapp']),
                InlineKeyboardButton(text='📞 Viber', url=urls['viber'])
            ],
            [
                InlineKeyboardButton(text='✈️ Telegram', url=urls['telegram']),
                InlineKeyboardButton(text='🔍 CallApp', url=urls['callapp'])
            ]
        ])

        # Формируем красивый ответ
        response = format_response(phone_info, ip_address, mailru_data, site_data, callapp_data)

        await message.answer(response, parse_mode='HTML', reply_markup=keyboards_start, disable_web_page_preview=True)

    except Exception as e:
        await message.answer(f"❌ Произошла ошибка при обработке контакта: {str(e)}")


# Вспомогательные функции
async def fetch_url(url: str, timeout: int = 10):
    """Асинхронно получает содержимое URL"""
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers, timeout=timeout) as response:
                return await response.text()
    except:
        return None


def parse_callapp(html_content):
    """Парсит данные с CallApp"""
    if not html_content:
        return "Не найдено"
    soup = BeautifulSoup(html_content, 'html.parser')
    number_elem = soup.find(class_='number')
    return number_elem.text.replace(" ", "").strip() if number_elem else "Не найдено"


def parse_mailru(html_content):
    """Парсит данные с Mail.ru"""
    if not html_content:
        return "Не найдено"
    soup = BeautifulSoup(html_content, 'html.parser')
    users_list = soup.find(class_='b-search__users__list')
    return users_list.text if users_list else "Не найдено"


def parse_site(html_content):
    """Парсит данные с сайта"""
    if not html_content:
        return "Не найдено"
    soup = BeautifulSoup(html_content, 'html.parser')
    jumbotron = soup.find(class_='jumbotron')
    return jumbotron.text.strip() if jumbotron else "Не найдено"


def parse_ip(html_content):
    """Парсит IP-адрес"""
    if not html_content:
        return "Не определен"

    soup = BeautifulSoup(html_content, 'html.parser')
    ip_section = soup.find('div', class_='pt-[16px] border-t border-t-gray-300')

    if not ip_section:
        return "Не определен"

    ip_tag = ip_section.find('p', string=' IP адрес ')
    if ip_tag:
        ip_link = ip_tag.find_next('span').find('a')
        if ip_link:
            return ip_link.text

    return "Не определен"


def format_response(info, ip, mailru, site, callapp):
    """Форматирует ответ красивым образом"""
    return f"""
╔══════════════════════════
║ 📱 <b>ИНФОРМАЦИЯ О КОНТАКТЕ</b>
╠══════════════════════════
║
║ 👤 <b>Личные данные:</b>
║ ├─ Имя: {info['first_name']}
║ ├─ Фамилия: {info['last_name']}
║ └─ ID: <code>{info['user_id']}</code>
║
║ 📞 <b>Номер телефона:</b>
║ ├─ Номер: <code>{info['raw']}</code>
║ ├─ Валидный: {'✅ Да' if info['is_valid'] else '❌ Нет'}
║ ├─ Возможный: {'✅ Да' if info['is_possible'] else '❌ Нет'}
║ └─ Оператор: {info['carrier']}
║
║ 🌍 <b>Геоданные:</b>
║ ├─ Регион: {info['region'] or 'Не определен'}
║ ├─ Страна: {info['timezone'][0] if info['timezone'] else 'Не определена'}
║ └─ IP адрес: <code>{ip}</code>
║
║ 🔍 <b>Дополнительная информация:</b>
║ ├─ CallApp: {callapp}
║ ├─ Mail.ru: {mailru[:50]}{'...' if len(mailru) > 50 else ''}
║ └─ Сайт: {site[:50]}{'...' if len(site) > 50 else ''}
║
╚══════════════════════════
    """

@router.message(F.text == '📧 E-mail')
async def email_osint(message: Message, state: FSMContext):
    await message.answer('Введи email 👤 обидчика')
    await state.set_state(Email.email)


@router.message(Email.email)
async def email_ok(message: Message, state: FSMContext):
    await message.answer("🔎 Идет поиск информации...")
    email = message.text.strip()
    username = email.split('@')[0]

    mail_ru_domains = ['@mail.ru', '@list.ru', '@bk.ru', '@gmail.ru']

    if any(domain in email for domain in mail_ru_domains):
        url = f'https://getscam.com/email/{email}'

        try:
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
        except requests.RequestException as e:
            await message.answer(f"❌ Ошибка при запросе: {str(e)}")
            await state.clear()
            return

        soup = BeautifulSoup(response.content, 'html.parser')

        # Находим блок с информацией
        info_block = soup.find('div', class_='pt-[16px] border-t border-t-gray-300')

        try:
            # Email
            email_tag = info_block.find('span', string=lambda x: x and '@' in x)
            found_email = email_tag.text.strip() if email_tag else email

            # Город
            city_tag = info_block.find('a', href=lambda x: x and 'find-city' in x)
            city = city_tag.text.strip() if city_tag else 'Не указан'

            # Домен
            domain_tag = info_block.find_all('span')
            domain = 'mail.ru'  # По умолчанию
            for span in domain_tag:
                if span.text.strip() in ['mail.ru', 'inbox.ru', 'list.ru', 'bk.ru', 'gmail.ru']:
                    domain = span.text.strip()
                    break

            # Телефон
            phone_tag = info_block.find('span', string=lambda x: x and '+7' in x)
            phone = phone_tag.text.strip() if phone_tag else 'Скрыт'

            # IP адрес
            ip_tag = info_block.find('a', href=lambda x: x and '/ip/' in x)
            ip = ip_tag.text.strip() if ip_tag else 'Не указан'

            # Страна
            country_tag = info_block.find_all('span')
            country = 'Россия'  # По умолчанию
            for span in country_tag:
                if span.text.strip() in ['Россия', 'Украина', 'Беларусь', 'Казахстан']:
                    country = span.text.strip()
                    break

            # Язык устройства
            lang_tag = info_block.find_all('span')
            language = 'RU'  # По умолчанию
            for span in lang_tag:
                if span.text.strip() in ['RU', 'EN', 'UA']:
                    language = span.text.strip()
                    break

            # Состояние
            status_tag = info_block.find_all('span')
            status = 'Обслуживается'  # По умолчанию
            for span in status_tag:
                if span.text.strip() in ['Обслуживается', 'Заблокирован', 'Неактивен']:
                    status = span.text.strip()
                    break

            # Формируем сообщение
            result_message = (
                f"<b>📧 Информация по email: {found_email}</b>\n\n"
                f"<b>━━━━━━━━━━━━━━━━━━━━━</b>\n\n"
                f"<b>🏢 Город:</b> {city}\n"
                f"<b>🌐 Домен:</b> {domain}\n"
                f"<b>👥 Социальные сети:</b> Скрыт\n"
                f"<b>📱 Телефон:</b> {phone}\n\n"
                f"<b>🏠 Адрес:</b> Скрыт\n"
                
                f"<b>🖥️ IP адрес:</b> <code>{ip}</code>\n"
                f"<b>🌍 Страна:</b> {country}\n\n"
                f"<b>🔤 Язык устройства:</b> {language}\n"
                f"<b>⚡ Состояние:</b> {status}\n\n"
                f"<b>━━━━━━━━━━━━━━━━━━━━━</b>\n"
            )

        except Exception as e:
            await message.answer(f"❌ Ошибка при парсинге: {str(e)}")
            await state.clear()
            return

        # Клавиатура с соцсетями
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text='📺 YouTube', url=f'https://www.youtube.com/results?search_query={email}'),
             InlineKeyboardButton(text='📘 Facebook', url=f'https://www.facebook.com/search/people/?q={email}')],
            [InlineKeyboardButton(text='🎵 TikTok', url=f'https://www.tiktok.com/search?q={email}'),
             InlineKeyboardButton(text='📱 VK', url=f'https://vk.com/search?c%5Bq%5D={username}&c%5Bsection%5D=people')],
            [InlineKeyboardButton(text='✈️ Telegram', url=f'https://t.me/{username}'),
             InlineKeyboardButton(text='📸 Instagram', url=f'https://www.instagram.com/{username}')],
            [InlineKeyboardButton(text='🎮 Roblox', url=f'https://www.roblox.com/search/users?keyword={username}'),
             InlineKeyboardButton(text='🐦 Twitter', url=f'https://twitter.com/search?q={username}&f=user')],
        ])

        await message.answer(result_message, parse_mode='HTML', reply_markup=keyboard)
        await state.clear()

    else:
        await message.answer(
            '❌ Этот email не поддерживается. Поддерживаются только домены: @mail.ru, @inbox.ru, @list.ru, @bk.ru, @gmail.ru',
            reply_markup=start_mes)
        await state.clear()


@router.message(F.text == 'Поиск по номеру 📱')
async def tele_osint(message: Message, state: FSMContext):
    await state.set_state(TeleOsint.telephone)
    await message.answer('Введи номер мобильного 📱 телефона жертвы 😭🥷. ')


@router.message(TeleOsint.telephone)
async def tele_infa(message: Message, state: FSMContext):
    # Начало поиска
    bot_message = await message.answer("🔍 Идет поиск информации...")
    await state.update_data(telephone=message.text)
    gomelin_anket_url = ''
    # Проверка премиум статуса
    db = SessionLocal()
    try:
        user = db.query(User).filter(User.telegram_id == str(message.from_user.id)).first()
        premium_by_us = user.premium if user else False
    finally:
        db.close()

    # Очистка номера телефона
    phone = message.text.replace('-', '').replace(' ', '').replace('+', '')

    # Валидация
    if not phone or len(phone) < 10:
        await message.answer("🤖 Введите корректный номер телефона 📱")
        await state.clear()
        return

    # Парсинг номера
    try:
        phone_number = phonenumbers.parse(f'+{phone}')
        geocoder1 = geocoder.description_for_number(phone_number, "ru")
        carrier1 = carrier.name_for_number(phone_number, 'ru')
        timezone1 = timezone.time_zones_for_number(phone_number)
        valid = 'Да' if phonenumbers.is_valid_number(phone_number) else 'Нет'
        possible = phonenumbers.is_possible_number(phone_number)
    except:
        await message.answer("🤖 Не удалось распознать номер")
        await state.clear()
        return

    # Инициализация переменных
    informatio_fio = 'Не найдено'
    informatio_fio_mts = 'Информация не найдена'
    telephone_from_mts = 'Информация не найдена'
    sure_name = 'Информация не найдена'
    date_of_birthday = "Не найдено"
    elements_info = 'Не найдено'
    element_school = 'Информация не найдена'
    elem_vk_id = 'Не найдено'
    profile_url_result = 'Не найдено'
    vk_profile_info = 'Не найдено'

    # Данные по регионам
    region_data = {
        'Минск': 'Не найдено',
        'Витебск': 'Не найдено',
        'Гродно': 'Не найдено',
        'Брест': 'Не найдено',
        'Гомель': 'Не найдено',
        'Могилев': 'Не найдено'
    }

    # Поиск по справочнику
    try:
        link_sparochnik = f'http://i.spravkaru.net/results2.php?page=1&sorts=phone&city_id=352&phone={phone[-7:]}&phonecons=full&lastname=&initials=&lastnamecons=part'
        response = requests.get(link_sparochnik, headers=headers, timeout=10)
        soup = BeautifulSoup(response.content, 'html.parser')

        text_table = soup.find(class_='%s')
        if text_table:
            informatio_fio = text_table.text.replace('-', '').replace(phone[-7:], '')
    except:
        pass

    # Поиск по МТС
    if carrier1 == 'МТС':
        try:
            link = f'https://spravochnik109.link/byelarus/mobilnaya-svyaz/mTS-mobilnyj-opyerator/mTS-mobilnyye-tyelyefony?phone={phone[-7:]}&streetSubStr=1&page=1&sort=1#menu'
            response = requests.get(link, headers=headers, timeout=10)
            soup = BeautifulSoup(response.content, 'html.parser')

            fio_element = soup.find('td', class_='fio')
            if fio_element:
                informatio_fio_mts = fio_element.text
                phone_element = soup.find('td', class_='adr')
                if phone_element:
                    telephone_from_mts = phone_element.text.strip()
        except:
            pass

    # Поиск в Велком и дополнительная информация
    try:
        link = f'https://spravochnik109.link/byelarus/mobilnaya-svyaz/vyelkom-mobilnyj-opyerator/vyelkom-mobilnyye-tyelyefony?phone=%2B{phone}&phoneSubStr=0&soname=&io=&sonameSubStr=0&street=&streetSubStr=1&house=&housing=&door=&page=1#google_vignette'
        response = requests.get(link, headers=headers, timeout=10)
        soup = BeautifulSoup(response.content, 'html.parser')

        # Адрес
        telephone_txt = soup.find('td', class_='adr')
        telephone_txt = telephone_txt.text if telephone_txt else ''

        # ФИО
        text_fio = soup.find(class_='res')
        if text_fio:
            fio_name = text_fio.text
            fio_text = fio_name.replace("Телефоны", "").strip()
            name_user = re.sub(r'[^\w\s]+|[\d]+', r'', fio_text)
            sure_name = name_user.replace(' XXX', '')

            # Поиск по регионам
            regions = {
                'Минск': f'https://spravochnik109.link/byelarus/minskaya-oblast/oblastnoj-tsyentr/minsk?phone=%2B{phone}&phoneSubStr=0&soname=&io=&sonameSubStr=0&street=&streetSubStr=1&house=&housing=&door=&page=1#menu',
                'Витебск': f'https://spravochnik109.link/byelarus/vityebskaya-oblast/oblastnoj-tsyentr/vityebsk?phone={phone[-6:]}&phoneSubStr=0&soname=&io=&sonameSubStr=0&street=&streetSubStr=1&house=&housing=&door=&page=1#menu',
                'Гродно': f'https://spravochnik109.link/byelarus/grodnyenskaya-oblast/oblastnoj-tsyentr/grodno?phone={phone[-6:]}&phoneSubStr=0&soname=&io=&sonameSubStr=0&street=&streetSubStr=1&house=&housing=&door=&page=1#menu',
                'Брест': f'https://spravochnik109.link/byelarus/bryesTSkaya-oblast/oblastnoj-tsyentr/bryest?phone={phone[-6:]}&phoneSubStr=0&soname=&io=&sonameSubStr=0&street=&streetSubStr=1&house=&housing=&door=&page=1#menu',
                'Гомель': f'https://spravochnik109.link/byelarus/gomyelskaya-oblast/oblastnoj-tsyentr/gomyel?phone={phone[-6:]}&phoneSubStr=0&soname=&io=&sonameSubStr=0&street=&streetSubStr=1&house=&housing=&door=&page=1#menu',
                'Могилев': f'https://spravochnik109.link/byelarus/mogilyevskaya-oblast/oblastnoj-tsyentr/mogilyev?phone={phone[-6:]}&phoneSubStr=0&soname=&io=&sonameSubStr=0&street=&streetSubStr=1&house=&housing=&door=&page=1#menu'
            }

            for city, url in regions.items():
                try:
                    resp = requests.get(url, headers=headers, timeout=5)
                    city_soup = BeautifulSoup(resp.content, 'html.parser')
                    city_fio = city_soup.find('td', class_='fio')
                    if city_fio:
                        city_addr = city_soup.find('td', class_='adr')
                        addr_text = city_addr.text if city_addr else ''
                        region_data[city] = f'<a href="tg://copy?text=">{city_fio.text.strip()}</a> Адрес: {addr_text}'
                except:
                    pass

            # Поиск на Gomelin
            if len(sure_name.split()) >= 2:
                parts = sure_name.split()
                surname_class = parts[0]
                named_class = parts[1]

                url_linked = f'https://gomelin.com/?first_name={named_class}&last_name={surname_class}&country={geocoder1}&city=&birth_year=&submit=Начать+поиск#h'

                try:
                    resp = requests.get(url_linked, headers=headers, timeout=10)
                    name_soup = BeautifulSoup(resp.content, 'html.parser')

                    # Берем первый элемент short-item
                    first_item = name_soup.find('div', class_='short-item')

                    if first_item:
                        # Получаем ссылку на профиль из кнопки "Анкета"
                        profile_link = first_item.find('a', class_='profile-item__detail')
                        if profile_link and profile_link.get('href'):
                            profile_url = f'https://gomelin.com{profile_link.get("href")}'
                            profile_url_result = profile_url
                            gomelin_anket_url = profile_url

                            # Переходим по ссылке профиля
                            prof_resp = requests.get(profile_url, headers=headers, timeout=10)
                            prof_soup = BeautifulSoup(prof_resp.content, 'html.parser')

                            # Парсим информацию из div с классом fdesc full-text clearfix
                            info_div = prof_soup.find('div', class_='fdesc full-text clearfix')
                            if info_div:
                                vk_profile_info = info_div.text.strip()

                                # Извлекаем дату рождения из текста
                                if 'рождения' in vk_profile_info:
                                    # Ищем дату в формате "дд.мм" или "дд месяц"
                                    date_match = re.search(r'(\d{1,2}\.\d{1,2})|\d{1,2}\s+\w+', vk_profile_info)
                                    if date_match:
                                        date_of_birthday = date_match.group()

                                # Извлекаем имя и фамилию из текста
                                name_match = re.search(r'Страница\s+([А-Яа-я]+\s+[А-Яа-я]+)', vk_profile_info)
                                if name_match and sure_name == 'Информация не найдена':
                                    sure_name = name_match.group(1)

                                # Извлекаем VK ID если есть
                                vk_id_match = re.search(r'ID\s+(\d+)', vk_profile_info)
                                if vk_id_match:
                                    elem_vk_id = vk_id_match.group(1)

                                # Извлекаем местоположение
                                location_match = re.search(r'Местоположение:.*?>(.*?)<', vk_profile_info, re.DOTALL)
                                if not location_match:
                                    location_match = re.search(r'Местоположение:\s*(.+?)(?:\n|$)', vk_profile_info)
                                if location_match:
                                    elements_info = location_match.group(1).strip()

                except Exception as e:
                    print(f"Ошибка при парсинге Gomelin: {e}")
    except:
        pass

    # Генерация email
    num_dump = random.randint(0, 6)
    emails = []
    for _ in range(num_dump + 1):
        emails.append(fake.email().replace('@example.net', '@gmail.com'))
    text_email = ' '.join(emails)

    # Формирование ссылок
    tg_chat = f'https://t.me/{phone}'

    # Клавиатура
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='🟢 WhatsApp', url=f'https://wa.me/{phone}'),
         InlineKeyboardButton(text='🟣 Viber', url=f'https://viber.click/{phone}')],
        [InlineKeyboardButton(text='🔵 Telegram', url=tg_chat),
         InlineKeyboardButton(text='🔴 Сайт', url='https://tg-user.id/from/username/')]
    ])

    # Формирование текста ответа
    if sure_name == 'Информация не найдена' and informatio_fio_mts == 'Информация не найдена':
        # Нет никаких данных
        text_osint = (f'<b>Поиск 🤖💻📱 прошел успешно</b>:\n\n'
                      f'├ Телефон: {message.text}\n'
                      f'├ Оператор: {carrier1}\n'
                      f'├ Тип: mobile\n'
                      f'├ Регион: {timezone1}\n'
                      f'├ Страна: {geocoder1}\n'
                      f'├ Валид: {valid}\n'
                      f'└ Существует: {possible}\n\n'
                      f'📧 E-mail: {text_email}\n'
                      f'📝 Телефонные книги: None\n\n'
                      f'Ссылка: {tg_chat}')

    elif sure_name == 'Информация не найдена' and premium_by_us:
        # Только МТС данные и премиум
        text_osint = (f'<b>Поиск 🤖💻📱 прошел успешно</b>:\n\n'
                      f'├ Телефон: {message.text}\n'
                      f'├ Оператор: {carrier1}\n'
                      f'├ Тип: mobile\n'
                      f'├ Регион: {timezone1}\n'
                      f'├ Страна: {geocoder1}\n'
                      f'├ Валид: {valid}\n'
                      f'└ Существует: {possible}\n\n'
                      f'🔎 Поиск по МТС:\n'
                      f'├ 👤 ФИО: <a href="tg://copy?text={informatio_fio_mts}">{informatio_fio_mts}</a>\n'
                      f'├ 🌐 VK: <a href="https://vk.com/search/people?q={informatio_fio_mts}">Ссылка на VK здесь</a>\n'
                      f'├ 🏠 Адрес: <a href="tg://copy?text={telephone_from_mts}">{telephone_from_mts}</a>\n\n'
                      f'📧 E-mail: {text_email}\n'
                      f'📝 Телефонные книги: None\n\n'
                      f'Ссылка: {tg_chat}')

    elif informatio_fio_mts == 'Информация не найдена' and premium_by_us:
        # Только Велком данные и премиум
        regions_text = ''
        for city, data in region_data.items():
            regions_text += f'├ {city}: {data}\n'

        vk_link = f'https://vk.com/search/people?q={sure_name}'

        text_osint = (f'<b>Поиск 🤖💻📱 прошел успешно</b>:\n\n'
                      f'├ Телефон: {message.text}\n'
                      f'├ Оператор: {carrier1}\n'
                      f'├ Тип: mobile\n'
                      f'├ Регион: {timezone1}\n'
                      f'├ Страна: {geocoder1}\n'
                      f'├ Валид: {valid}\n'
                      f'└ Существует: {possible}\n\n'
                      f'<b>Основные:</b>\n'
                      f'├ 👤 ФИО: <a href="tg://copy?text={sure_name}">{sure_name}</a>\n'
                      f'├ Дата рождения: <i>{date_of_birthday}</i>\n'
                      f'├ 🌐 VK: <a href="{vk_link}">Ссылка на VK здесь</a>\n'
                      f'├ 🏠 ФИО и Адрес: <a href="tg://copy?text={informatio_fio},{telephone_txt}">{informatio_fio.strip()},{telephone_txt.strip()}</a>\n\n'
                      f'<b>👁️ Возможные Люди (домашний телефон {phone[-6:]})</b>:\n{regions_text}\n\n'
                      f'📧 E-mail: {text_email}\n'
                      f'👤 Возможные анкеты:\n'
                      f'├ 🏫 Образование:\n{element_school.strip()}\n'
                      f'├ 🌐 Vk: <a href="https://vk.com/{elem_vk_id}">Ссылка на VK здесь</a>\n'
                      f'├ 🔗 Ссылка на профиль: <a href="{profile_url_result}">Ссылка</a>\n'
                      f'├ 📝 Дополнительная информация:\n<a href="tg://copy?text={gomelin_anket_url}">{vk_profile_info.replace('Местоположение: Определить местоположение по номеру телефона','')}</a>\n\n'
                      f'📝 Телефонные книги: None\n\n'
                      f'Ссылка: {tg_chat}')

    elif premium_by_us:
        # Полные данные с премиумом
        regions_text = ''
        for city, data in region_data.items():
            regions_text += f'├ {city}: {data}\n'

        vk_link = f'https://vk.com/search/people?q={sure_name}'

        text_osint = (f'<b>Поиск 🤖💻📱 прошел успешно</b>:\n\n'
                      f'├ Телефон: {message.text}\n'
                      f'├ Оператор: {carrier1}\n'
                      f'├ Тип: mobile\n'
                      f'├ Регион: {timezone1}\n'
                      f'├ Страна: {geocoder1}\n'
                      f'├ Валид: {valid}\n'
                      f'└ Существует: {possible}\n\n'
                      f'<b>Основные:</b>\n'
                      f'├ 👤 ФИО: <a href="tg://copy?text={sure_name}">{sure_name}</a>\n'
                      f'├ Дата рождения: <i>{date_of_birthday}</i>\n'
                      f'├ 🌐 VK: <a href="{vk_link}">Ссылка на VK здесь</a>\n'
                      f'├ 🏠 ФИО и Адрес: <a href="tg://copy?text={informatio_fio},{telephone_txt}">{informatio_fio.strip()},{telephone_txt.strip()}</a>\n\n'
                      f'🔎 Поиск по МТС:\n'
                      f'├ 👤 ФИО: <a href="tg://copy?text={informatio_fio_mts}">{informatio_fio_mts}</a>\n'
                      f'├ 🏠 Адрес: <a href="tg://copy?text={telephone_from_mts}">{telephone_from_mts}</a>\n\n'
                      f'<b>👁️ Возможные Люди (домашний телефон {phone[-6:]})</b>:\n{regions_text}\n\n'
                      f'📧 E-mail: {text_email}\n'
                      f'👤 Возможные анкеты:\n'
                      f'├ 🔗 Ссылка на профиль: <a href="{profile_url_result}">Ссылка</a>\n'
                      f'├ 📝 Дополнительная информация:\n<a href="tg://copy?text={gomelin_anket_url}">{vk_profile_info.replace('Местоположение: Определить местоположение по номеру телефона','')}</a>\n\n'
                      f'📝 Телефонные книги: None\n\n'
                      f'Ссылка: {tg_chat}')
    else:
        # Бесплатная версия
        text_osint = (f'<b>Поиск 🤖💻📱 прошел успешно</b>:\n\n'
                      f'├ Телефон: {message.text}\n'
                      f'├ Оператор: {carrier1}\n'
                      f'├ Тип: mobile\n'
                      f'├ Регион: {timezone1}\n'
                      f'├ Страна: {geocoder1}\n'
                      f'├ Валид: {valid}\n'
                      f'└ Существует: {possible}\n\n'
                      f'📧 E-mail: {text_email}\n'
                      f'📝 Телефонные книги: None\n\n'
                      f'Ссылка: {tg_chat}\n'
                      f'<b>🔃 Чтобы узнать больше, нужно купить 🔑 Подписку</b>')

    # Отправка результата
    await message.reply(text_osint, parse_mode='HTML', reply_markup=keyboard)

    # Дополнительный поиск для российских номеров
    if phone.startswith('7'):
        try:
            # Поиск IP
            url = f'https://getscam.com/{phone}'
            response = requests.get(url, headers=headers, timeout=10)
            soup = BeautifulSoup(response.content, 'html.parser')

            ip_element = soup.find(class_='top__info-item')
            if ip_element:
                ip_text = ip_element.text
                ip_start = ip_text.find('IP адрес')
                if ip_start != -1:
                    ip_start += len('IP адрес')
                    ip_end = ip_text.find('Сайт оператора', ip_start)
                    ip_address = ip_text[ip_start:ip_end].strip()

                    if ip_address != "Не найден":
                        # Информация о компании
                        tinkoff_url = f'https://www.tbank.ru/oleg/who-called/info/{phone}/'
                        tinkoff_resp = requests.get(tinkoff_url, headers=headers, timeout=10)
                        tinkoff_soup = BeautifulSoup(tinkoff_resp.content, 'html.parser')
                        company = tinkoff_soup.find(class_='abtnK6gFv')
                        company_text = company.text if company else 'Не найдено'

                        # Геоданные IP
                        ip_response = requests.get(f'http://ip-api.com/json/{ip_address}').json()

                        ip_message = (f"Поиск по IP прошел успешно ✅\n\n"
                                      f"IP: {ip_address}\n"
                                      f"├ Провайдер: {ip_response.get('isp')}\n"
                                      f"├ Организация: {ip_response.get('org')}\n"
                                      f"├ Страна: {ip_response.get('country')}\n"
                                      f"├ Регион: {ip_response.get('regionName')}\n"
                                      f"├ Город: {ip_response.get('city')}\n"
                                      f"├ Широта: {ip_response.get('lat')}\n"
                                      f"└ Долгота: {ip_response.get('lon')}\n\n"
                                      f"🏢 Предприятие: {company_text}")

                        await message.answer(ip_message, parse_mode='HTML')
        except:
            pass

    await asyncio.sleep(1)
    await message.answer('✅ Поиск закончен. Все данные выше.', reply_markup=start_mes)
    await state.clear()


@router.message(F.content_type == ContentType.PHOTO)
async def search_photo(message: Message):
    search_site = 'https://search4faces.com'
    google_search = 'https://images.google.com'
    yandex_search = 'https://yandex.ru/images/'

    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='👁 Yandex', url=yandex_search),
         InlineKeyboardButton(text='👁 Google', url=google_search)],
        [InlineKeyboardButton(text='👁 Сайт', url=search_site)]
    ])
    await message.answer('🔎 Фото человека можно найти ниже ⬇️', reply_markup=keyboard)


@router.message(Command('send'))
async def send_message_start(message: Message, state: FSMContext):
    await state.set_state(SendMessage.waiting_phone)
    await message.answer('📱 Введите номер телефона подключенного аккаунта:')


@router.message(SendMessage.waiting_phone)
async def process_phone(message: Message, state: FSMContext):
    user_id = message.from_user.id
    phone = message.text.strip().replace(' ', '').replace('+', '')
    session_file = f'session_{phone}.txt'
    if user_id != ADMIN_ID:
        if phone == '375445389424':
            await message.answer('Ты совсем  ?')
            await state.clear()
            return
    if not os.path.exists(session_file):
        await message.answer('❌ Сессия не найдена. Сначала подключите аккаунт через 👤 Аккаунт')
        await state.clear()
        return

    try:
        with open(session_file, 'r') as f:
            session_string = f.read().strip()

        # Используем StringSession вместо файловой
        client = TelegramClient(
            StringSession(session_string),
            api_id,
            api_hash
        )
        await client.connect()

        if not await client.is_user_authorized():
            await message.answer('❌ Сессия есть, но аккаунт не авторизован')
            await client.disconnect()
            os.remove(session_file)
            await state.clear()
            return

        me = await client.get_me()

        # Сохраняем клиент и данные
        await state.update_data(
            client=client,
            phone=phone,
            session_file=session_file,
            username=me.username
        )

        await message.answer(f'✅ Аккаунт @{me.username} найден! Теперь введите текст сообщения:')
        await state.set_state(SendMessage.waiting_text)

    except Exception as e:
        await message.answer(f'❌ Ошибка при подключении: {e}')
        # Удаляем битую сессию
        if os.path.exists(session_file):
            os.remove(session_file)
        await state.clear()


@router.message(SendMessage.waiting_text)
async def process_text(message: Message, state: FSMContext):
    text = message.text.strip()

    if len(text) == 0:
        await message.answer('❌ Текст не может быть пустым. Введите текст:')
        return

    await state.update_data(text=text)
    await message.answer(
        '💬 Текст сохранен! Теперь введите username чата или ID:\n\n'
        'Примеры:\n'
        '• @username\n'
        '• 123456789 (ID чата)\n'

    )
    await state.set_state(SendMessage.waiting_chat)


@router.message(SendMessage.waiting_chat)
async def process_chat_and_send(message: Message, state: FSMContext):
    chat_identifier = message.text.strip()
    data = await state.get_data()

    client = data.get('client')
    text = data.get('text')
    phone = data.get('phone')
    username = data.get('username', 'неизвестно')

    if not client or not text:
        await message.answer('❌ Ошибка данных. Начните заново.')
        await state.clear()
        return

    try:
        # Очищаем идентификатор чата
        if chat_identifier.startswith('https://t.me/'):
            chat_identifier = '@' + chat_identifier.split('/')[-1]
        elif chat_identifier.startswith('@'):
            chat_identifier = chat_identifier
        else:
            # Если это число, пробуем как ID
            try:
                chat_identifier = int(chat_identifier)
            except ValueError:
                chat_identifier = '@' + chat_identifier.lstrip('@')

        # Отправляем сообщение
        await client.send_message(chat_identifier, text)

        await message.answer(f'✅ Сообщение отправлено!\n\n📱 Аккаунт: @{username}\n💬 Чат: {chat_identifier}\n')

    except Exception as e:
        await message.answer(f'Ошибка  в {e}')

    finally:
        # Всегда отключаем клиент и очищаем состояние

        await client.disconnect()

        await state.clear()


@router.message(F.text == '🔎 Поиск по IP')
async def ip_osint(message: Message, state: FSMContext):
    await state.set_state(Ip.ip_adress)
    await message.answer('Введите Ip адресс жертвы', reply_markup=ip_get)


@router.message(Ip.ip_adress)
async def ip_search(message: Message, state: FSMContext):
    bot_message = await message.answer('Идет поиск 🔎 информации...')
    await state.update_data(ip_adress=message.text)
    ip = message.text.strip()

    response = requests.get(url=f'http://ip-api.com/json/{ip}').json()
    country = response.get('country')
    if len(ip) < 10:
        await message.answer('Введи Ip коректно...')
        await state.clear()
    elif country is None:
        await message.answer('Увы информация не 📝 найдена. Такого IP не существует 💣.', reply_markup=start_mes)
        await state.clear()
    else:

        try:

            text = f"Поиск  ️🤖💻📱 прошел успешно:\n\nIP: {ip}\n├ Провайдер: {response.get('isp')}\n├ Организация: {response.get('org')}\n├ Ofset: {response.get('offset')}\n├ Валюта: {response.get('BYR')}\n├ As: {response.get('as')}\n├ As_name: {response.get('asname')}\n├ Мобильный ip:{response.get('mobile')}\n├ Прокси: {response.get('proxy')}\n├ Hosting: {response.get('hosting')}\n├ DNS:{response.get('dns')}\n├ Континент: {response.get('continentCode')}\n├ Страна: {response.get('country')}\n├ Регион: {response.get('regionName')}\n├ Город: {response.get('city')}\n├ ZIP: {response.get('zip')}\n├ Широта: {response.get('lat')}\n└ Долгота: {response.get('lon')}"

            await bot_message.edit_text(text)
            await asyncio.sleep(2)
            coordinates = f"{response.get('lat')},{response.get('lon')}"
            nominaltim = Nominatim(user_agent='user')
            location = nominaltim.reverse(coordinates)

            await message.answer_location(latitude=response.get('lat'), longitude=response.get('lon'))
            await message.answer(f'-- Поиск по координатам 🌍:\n\n{str(location)}', reply_markup=start_mes)

        except requests.exceptions.ConnectionError:
            await message.answer('Увы информация не найдена')
        await state.clear()


@router.message(F.text == '👁️ Поиск username')
async def user_name_osint(message: Message, state: FSMContext):
    await message.answer('Введите username который вы хотите узнать.')
    await state.set_state(Username.username)


@router.message(Username.username)
async def user_name_over(message: Message, state: FSMContext):
    username = message.text.strip()
    if username == '':
        await message.answer('Ваш username не распознан', reply_markup=start_mes)
        await state.clear()
        return

    if len(username) > 20:
        await message.answer('Ваш username превышает лимит', reply_markup=start_mes)
        await state.clear()
        return
    username = username.replace('@', '')
    text_github = 'None'
    try:
        response = requests.get(f"https://api.github.com/users/{username}", headers=headers)
        if response.status_code == 200:
            data = response.json()

            text_github = (
                f"├ Name: {data.get('name')}\n├ Bio: {data.get('bio')}\n├ Location: {data.get('location')}\n├ Public_repos: {data.get('public_repos')}\n├ Profile: {data.get('html_url')}\n├ Email: {data.get('email')} "

            )
    except:
        print(f"None in Github")

    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='Instagram', url=f'https://www.instagram.com/{username}/'),
         InlineKeyboardButton(text='  Twitch', url=f'https://www.twitch.tv/{username}')],
        [InlineKeyboardButton(text=' Facebook', url=f'https://www.facebook.com/{username}'),
         InlineKeyboardButton(text=' Twitter', url=f'https://x.com/{username}')],

        [InlineKeyboardButton(text='  Vimeo', url=f'https://vimeo.com/{username}'),
         InlineKeyboardButton(text='Linkedln', url=f'https://www.linkedin.com/{username}')],
        [InlineKeyboardButton(text=' Github', url=f'https://github.com/{username}'),
         InlineKeyboardButton(text='  Steam', url=f'https://steamcommunity.com/groups/{username}')],
        [InlineKeyboardButton(text=' Minecraft', url=f'https://minecraftuuid.com/?search={username}'),
         InlineKeyboardButton(text='  Xbox', url=f'https://xboxgamertag.com/search/{username}')],
        [InlineKeyboardButton(text='🔵 Telegram', url=f'https://t.me/{username}',style='primary',icon_custom_emoji_id='5436302963117137450')],
        [InlineKeyboardButton(text='🔴  Youtube', url=f'https://www.youtube.com/@{username}',style='danger',icon_custom_emoji_id='5359523920120651432')],
        [InlineKeyboardButton(text=' Spotify', url=f'https://open.spotify.com/user/{username}'),
         InlineKeyboardButton(text=' Replit', url=f'https://replit.com/@{username}')],
        [InlineKeyboardButton(text='  Rumble', url=f'https://rumble.com/user/{username}'),
         InlineKeyboardButton(text=' Hacker', url=f'https://news.ycombinator.com/user?id={username}')],
        [InlineKeyboardButton(text=' Snapchat', url=f'https://www.snapchat.com/@{username}'),
         InlineKeyboardButton(text=' Reddit', url=f'https://www.reddit.com/user/{username}/')],

        [InlineKeyboardButton(text=' Blusky', url=f'https://bsky.app/profile/{username}.bsky.social'),
         InlineKeyboardButton(text=' Gitlab', url=f'https://gitlab.com/{username}')],

    ])
    await asyncio.sleep(1.1)
    await message.answer(f'🔎 Поиск прошел успешно:\n\n👤 Username: <b>{username}</b>\n\n👥 Github:\n{text_github}',
                         parse_mode='HTML', reply_markup=keyboard)
    await state.clear()

@router.message(F.text == '💼 Dos')
async def ddos_start(message: Message, state: FSMContext):
    db = SessionLocal()

    # 1. Проверяем существующего пользователя
    user = db.query(User).filter(User.telegram_id == str(message.from_user.id)).first()
    premium_by_us = user.premium

    db.close()
    if premium_by_us is True:
        await state.set_state(Ddoss.target)
        await message.answer("Введите URL 🔎 жертвы 🌍💻 ")
    else:
        await state.clear()
        await message.answer("❌ У вас отсутствует 🔑 Подписка в боте")


@router.message(Ddoss.target)
async def ddos(message: Message, state: FSMContext):
    text = message.text.strip()
    if len(text) < 10:
        await message.answer('Это не URL попробуй заново.')
        await state.clear()

    if len(text) > 60:
        await message.answer('Это не URL попробуй заново.')
        await state.clear()

    if text.startswith(('http://', 'https://', 'www.')):
        await state.update_data(target=message.text)
        await state.set_state(Ddoss.number)

        await message.answer('Введи количество пакетов🛍️ не больше 100')
    else:
        await message.answer('Это не URL попробуй заново.')
        await state.clear()


@router.message(Ddoss.number)
async def ddosing(message: Message, state: FSMContext):
    await state.update_data(number=message.text)
    data = await state.get_data()
    target = data['target']

    sockets = int(message.text)
    print(target, sockets)
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
    await message.answer('Dos атака ⚔️🛍️💻 закончилась все данные вверху.', reply_markup=start_mes)
    await state.clear()


@router.message(F.text == '🕵️ ️Мой профиль')
async def profile(message: Message):
    db = SessionLocal()

    # 1. Проверяем существующего пользователя
    user = db.query(User).filter(User.telegram_id == str(message.from_user.id)).first()
    premium_by_us = user.premium
    user_register_at = user.register_at
    queries_user = user.queries
    db.close()

    if premium_by_us is True:
        premium_by_us = '✅'
    else:
        premium_by_us = '❌'

    await message.reply(
        f'ℹ️ Вся необходимая информация о вашем профиле\n\n🏷️ <b>Имя:</b> <a href="tg://copy?text=ddddd">{message.from_user.full_name}</a>\n🔗<b>Username:</b> @{message.from_user.username}\n\n🆔 <b>Мой ID:</b> <a href="tg://copy?text=ddddddd">{message.from_user.id}</a>\n📆 <b>Регистрация:</b> <a href="tg://copy?text=fdddd">{user_register_at}</a>\n🔃 <b>TG Премиум:</b> {message.from_user.is_premium}\n🧮 <b>Купленные запросы:</b> <a href="tg://copy?text=dddd">{queries_user}</a>\n\n🔑 <b>Подписка:</b> {premium_by_us}\n🗣️ <b>Язык:</b> <b>{message.from_user.language_code}</b>\n\n💰 Твой баланс: <a href="tg://copy?text=0.00">0.00 RUB</a>\n',
        reply_markup=json_user,parse_mode="HTML")


@router.callback_query(F.data == 'json')
async def json(callback: CallbackQuery):
    jsons = callback.from_user.json()
    await callback.answer('')
    await callback.message.answer(f"{jsons}")


@router.message(F.text == '👤 Аккаунт')
async def account_login(message: Message, state: FSMContext):
    await state.set_state(Account.phone_num)
    await message.answer('Введи номер телефона 📲', parse_mode='HTML')


@router.message(Account.phone_num)
async def account_log(message: Message, state: FSMContext):
    phone = message.text.strip().replace(' ', '').replace('+', '')  # убираем + для хранения
    session_file = f'session_{phone}.txt'

    # ... (проверка существующей сессии)

    try:
        session = StringSession()
        client = TelegramClient(session, api_id, api_hash)
        await client.connect()

        # ВАЖНО: добавляем + при отправке запроса кода
        send_code = await client.send_code_request(phone=f'+{phone}')  # ← ИСПРАВЛЕНО
        print(send_code.phone_code_hash, api_hash, api_id)

        await state.update_data(
            hashing=send_code.phone_code_hash,
            client=client,
            phone=phone,  # храним без + для имени файла
            session_string=session.save(),
            session_file=session_file
        )

        await message.answer('⬆️ Введи код с -100 в начале:')
        await state.set_state(Account.code)

    except Exception as e:
        await message.answer(f'❌ Ошибка: {e}')
        await state.clear()


@router.message(Account.code)
async def account_code_sent(message: Message, state: FSMContext):
    data = await state.get_data()

    session = StringSession(data['session_string'])
    client = TelegramClient(session, api_id, api_hash)
    await client.connect()

    code = message.text.strip().replace('-100', '')

    if len(code) != 5 or not code.isdigit():
        await message.answer("❌ Нужно 5 цифр после -100")
        await client.disconnect()
        return

    try:
        # ВАЖНО: добавляем + при входе с кодом
        await client.sign_in(
            phone=f'+{data["phone"]}',  # ← ИСПРАВЛЕНО
            code=code,
            phone_code_hash=data['hashing']
        )

        if await client.is_user_authorized():
            me = await client.get_me()
            await message.answer(
                f'✅ Аккаунт @{me.username} подключен!\n\n<b>Инструкция</b>:\n Чтобы начать нужно написать(.trolling)\n Чтобы остановить нужно написать(.stop).',
                parse_mode='HTML')

            session_string = session.save()
            with open(data['session_file'], 'w') as f:
                f.write(session_string)

            await setup_client_handlers(client)

    except SessionPasswordNeededError:
        session_string = session.save()
        await state.update_data(
            session_string=session_string,
            client=client
        )
        await message.answer('🔒 Введите пароль 2FA:')
        await state.set_state(Account.password)
        return

    except Exception as e:
        await message.answer(f'❌ Ошибка: {e}')
        await client.disconnect()

    await state.clear()


@router.message(Account.password)
async def password_sign_in(message: Message, state: FSMContext):
    data = await state.get_data()

    # Восстанавливаем клиент из строки сессии
    session = StringSession(data['session_string'])
    client = TelegramClient(
        session,
        api_id,
        api_hash
    )

    await client.connect()

    try:
        await client.sign_in(password=message.text.strip())

        if await client.is_user_authorized():
            me = await client.get_me()
            await message.answer(f'✅ Аккаунт @{me.username} подключен!')

            # Сохраняем сессию в файл
            session_string = session.save()  # ← ПРАВИЛЬНО!
            with open(data['session_file'], 'w') as f:
                f.write(session_string)

            await setup_client_handlers(client)
        else:
            await message.answer('❌ Не удалось авторизоваться')
            await client.disconnect()

    except Exception as e:
        await message.answer(f'❌ Ошибка: {e}')
        await client.disconnect()

    await state.clear()


async def setup_client_handlers(client):
    @client.on(events.NewMessage(pattern='.trolling'))
    async def handler(event):

        existing_text = "Я тебе сынку тупой шлюхи твое сосалище переломаю своим огромным палающим хуем ведь ты ебанная мразота которая сидит здесь и терпит нихуевые харчки в свое прищавое ебало которое я использовал как тряпку для пола ибо ты сын шалавы парокопытной вообще не можешь дать весомого отпора, ты как слабый чуркобес у которого мать шлюха ебанная будешь постоянно в роли терпилы сидеть и мой член мусолить своими обжогшими ручками ведь я не раз предупреждал что мой член разогревается до температуры солнца, но ты сын бляди ебанной все равно пытался дать отпор и каждый раз отлетал в нокаут после первого точного удара и моему члену уже было скучно каждый раз тебя пинком к дому отправлять поэтому я взял твое свинное рыло в руки и приложил к стене которая была вся в моей сперме, и начал ломать твое горящее очко набирая скорость всё выше и выше, щегол ебучий когда ты уже поймёшь что на меня рыпаться не нужно ибо ты сын шалавы будешь отрабатывать каждый пинок под зад который ты получаешь после очередного отсоса пытаясь побороться с моей шиповоной подошвой которая вся в дерьме, ты сын шлюхи косоеблой до конца своей жизни будешь стоять на коленях и умолять мой огромный член поправить наконец-то свой свинной спермоприемник на котором прищей больше чем у родной матери зубов, но он как и раньше будет заплевывать тежёлыми маслянистыми харчками  твое окровавленное ебало на котором дохуище шрамов от моего палающего члена который твоя матушка закидывает к себе в ротан как школьники снюс"
        words = existing_text.split()
        await event.delete()

        # Флаг для остановки
        stop_flag = False

        # Обработчик для команды stop
        @client.on(events.NewMessage(pattern='.stop'))
        async def stop_handler(stop_event):
            nonlocal stop_flag
            if stop_event.chat_id == event.chat_id:
                stop_flag = True

                await stop_event.delete()

            # Бесконечный цикл

        while not stop_flag:
            for i in range(0, len(words), 2):
                if stop_flag:
                    break
                pair = ' '.join(words[i:i + 2])
                await event.respond(pair)
                await asyncio.sleep(0.02)

                # Небольшая пауза между циклами
            if not stop_flag:
                await asyncio.sleep(1)

@router.message(Command('search_database'))
async def search_first_step(message:Message,state:FSMContext):
    await message.answer('📱Введите номер телефона который вы хотите найти')
    await state.set_state(Find.telephone)


@router.message(Find.telephone)
async def search_phoned(message: Message, state: FSMContext):

        telephone = message.text.strip().replace('+', '').replace(' ', '').replace('-', '')

        try:
            # Парсим номер с помощью phonenumbers
            parsed_number = phonenumbers.parse(telephone, "BY")

            # Проверяем валидность номера
            if not phonenumbers.is_valid_number(parsed_number):
                await message.answer("❌ <b>Неверный формат номера</b>\nПример: <code>375334760525</code>")
                return

            # Получаем национальный номер
            national_number = str(parsed_number.national_number)

            # Убираем код оператора (33 для МТС)
            if national_number.startswith('33'):
                short_number = national_number[2:]  # Убираем '33'
            else:
                short_number = national_number

            # Поиск в файле (MTS.txt на уровень выше)
            result = search_in_file(short_number, "data_file.txt")

            await message.answer(result, parse_mode="HTML")
            await state.clear()

        except phonenumbers.NumberParseException:
            await message.answer(
                "❌ <b>Ошибка!</b>\nНомер должен начинаться с <code>+37533</code>\nПример: <code>+375334760525</code>")
        except Exception as e:
            await message.answer(f"❌ <b>Ошибка:</b> {str(e)}")



@router.message(F.text == '👁️ Глаз Бога')
async def eye_of_god(message:Message,state:FSMContext):
    db = SessionLocal()
    user = db.query(User).filter(User.telegram_id == str(message.from_user.id)).first()
    premium_user = user.premium
    db.close()
    if premium_user is True:
       await message.answer('Введи номер мобильного 📱 телефона жертвы 😭🥷.')
       await state.set_state(God.phone)
       return
    else:
       await message.answer('❌ Чтобы использовать данную функцию нужно иметь 🔑 <b>Подписку</b>',parse_mode="HTML")
       return

@router.message(God.phone)
async def eye_of_god(message:Message,state:FSMContext):
    phone = message.text.strip().replace(' ','').replace('+','').replace('-','')

    db = SessionLocal()
    user = db.query(User).filter(User.telegram_id == str(message.from_user.id)).first()
    queries_user = user.queries

    if queries_user > 1:
        payload = {
           "token": "18baca3d-3abc-4f49-b91b-65eced749e29",
           "query": f"{phone}"
        }

        response = requests.post(
             "https://api.dyxless.at/query",
             json=payload,
             headers={"Content-Type": "application/json"}
        )
        data = response.json()
        text = ''
        status = data.get('status')
        if status is False:
            text = f'🔴 {data.get("message")}'
        else:
            text = f"<b>Поиск  ️🤖💻📱 прошел успешно</b>:\n👁️ Контент{data.get('data')}"

        await message.answer(f'{text}')
        await state.clear()

        user.queries = user.queries - 1
        db.commit()

    else:
        await message.answer(f'🔴 У вас не хватает запросов ,Подписку🔑 можно купить в конце месяца.')
        await state.clear()

    db.close()


@router.message(Command('search_vk'))
async def search_vk_account(message:Message,state:FSMContext):
    await message.answer('Введите id пользователя VK:')
    await state.set_state(Vk.vk_id)


@router.message(Vk.vk_id)
async def vk_searching(message: Message, state: FSMContext):
    user_vk_id = message.text.strip()

    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📷 Фото профиля", url=f"https://vk.com/albums{user_vk_id}")],
        [InlineKeyboardButton(text='🔵 Vk', url=f'https://vk.com/id{user_vk_id}')]
    ])

    try:
        user_data = vk.users.get(
            user_ids=f'{user_vk_id}',
            fields='bdate, city, country, contacts, sex, online, last_seen, relation, education, universities, schools, occupation, about, status, followers_count, verified, home_town, personal, site, activities, interests, music, movies, tv, books, games, counters'
        )

        if not user_data:
            await message.answer("❌ Пользователь не найден.")
            await state.clear()
            return

        user = user_data[0]

        def get_field(field, default='Не указано'):
            return user.get(field, default) or default

        # Базовые данные
        first_name = get_field('first_name')
        last_name = get_field('last_name')
        birthday = get_field('bdate')

        # Пол
        sex_map = {1: 'Женский', 2: 'Мужской', 0: 'Не указан'}
        sex = sex_map.get(get_field('sex', '0'), 'Не указан')

        # Онлайн статус
        online_status = '✅ Онлайн' if get_field('online') else '❌ Оффлайн'

        # Время последнего посещения
        last_seen = get_field('last_seen', 'не известно')
        last_seen_time = ''
        if last_seen and isinstance(last_seen, dict) and 'time' in last_seen:
            from datetime import datetime
            last_seen_dt = datetime.fromtimestamp(last_seen['time'])
            last_seen_time = last_seen_dt.strftime('%d.%m.%Y %H:%M')
        else:
            last_seen_time = 'Неизвестно'

        # Город
        city_name = 'Не указан'
        if 'city' in user and user['city']:
            city_name = user['city'].get('title', 'Не указан')

        # Родной город
        home_town = get_field('home_town')

        # Семейное положение
        relation_map = {
            1: 'Не женат/Не замужем',
            2: 'Есть друг/Есть подруга',
            3: 'Помолвлен/Помолвлена',
            4: 'Женат/Замужем',
            5: 'Всё сложно',
            6: 'В активном поиске',
            7: 'Влюблён/Влюблена',
            8: 'В гражданском браке',
            0: 'Не указано'
        }
        relation = relation_map.get(get_field('relation', '0'), 'Не указано')

        # Образование
        education_info = []
        if 'education' in user:
            edu = user['education']
            if edu.get('university_name'):
                education_info.append(f"🎓 {edu['university_name']}")

        # Университеты
        universities_info = []
        if 'universities' in user and user['universities']:
            for uni in user['universities'][:2]:
                name = uni.get('name', '')
                if name:
                    universities_info.append(f"🏫 {name}")

        # Работа
        work_info = ''
        occupation_info = get_field('occupation', 'не указано')
        if occupation_info and isinstance(occupation_info, dict):
            if occupation_info.get('type') == 'work':
                work_info = f"💼 {occupation_info.get('name', '')}"

        # О себе
        about = get_field('about')
        if about and len(about) > 150:
            about = about[:150] + "..."

        # Статус
        status = get_field('status')

        # Верификация
        verified = '✅ Да' if get_field('verified') else '❌ Нет'

        # Личная информация
        personal_info = []
        if 'personal' in user and user['personal']:
            personal = user['personal']
            if personal.get('religion'):
                personal_info.append(f"🙏 {personal['religion']}")

        # Счетчики
        counters_info = []
        if 'counters' in user and user['counters']:
            counters = user['counters']
            if counters.get('friends'):
                counters_info.append(f"👥 {counters['friends']}")
            if counters.get('photos'):
                counters_info.append(f"📷 {counters['photos']}")

        # Доступ к профилю
        can_access = user.get('can_access_closed', False)
        is_closed = user.get('is_closed', False)
        is_closed_text = 'Закрытый' if is_closed else 'Открытый'
        access_text = 'Есть' if can_access else 'Нет'

        # Формируем сообщение (простой текст)
        response_text = f'🔍<b> Результаты поиска VK</b>\n\n'

        response_text += f'<b>👤 Имя: {first_name}</b>\n'
        response_text += f'<b>👤 Фамилия: {last_name}</b>\n'
        response_text += f'<b>🚻 Пол: {sex}</b>\n'
        response_text += f'<b>🆔 ID:</b> <a href="tg://copy?text={user_vk_id}">{user_vk_id}</a>\n\n'

        response_text += f'{online_status}\n'
        response_text += f'<b>📅 Последний раз:</b> <a href="tg://copy?text={last_seen_time}">{last_seen_time}</a>\n'
        response_text += f'<b>✅ Верификация:</b> {verified}\n\n'

        response_text += f'<b>🏛️ Город: {city_name}</b>\n'
        if home_town != 'Не указано' and home_town != city_name:
            response_text += f'📍<b> Родной город: {home_town}</b>\n'

        response_text += f'📅<b> Дата рождения:</b> <a href="tg://copy?text={birthday}">{birthday}</a>\n'
        response_text += f'💍 <b>Семейное положение: {relation}</b>\n'

        if personal_info:
            response_text += f'📌<b> Личное: {", ".join(personal_info)}</b>n'

        if about != 'Не указано':
            response_text += f'\n📝<b> О себе:</b>\n<i>{about}</i>\n'

        if status != 'Не указано' and status:
            response_text += f'\n💬<b> Статус:</b>\n{status}\n'

        # Образование и работа
        if education_info or universities_info or work_info:
            response_text += f'\n🎓<b> Образование и работа:</b>\n'
            for edu in education_info:
                response_text += f'{edu}\n'
            for uni in universities_info:
                response_text += f'{uni}\n'
            if work_info:
                response_text += f'{work_info}\n'

        # Счетчики
        if counters_info:
            response_text += f'\n📊<b> Активность:</b>\n'
            response_text += f' | '.join(counters_info) + '\n'

        response_text += f'\n<b>🔐 Профиль: {is_closed_text}</b>\n'
        response_text += f'<b>🔓 Доступ: {access_text}</b>'

        # Отправляем сообщение
        await message.answer(response_text, parse_mode='HTML', reply_markup=keyboard)

    except Exception:
        await message.answer(
            f"❌ Ошибка при поиске\n"
            f"Проверьте правильность ID и попробуйте снова."
        )

    await state.clear()

@router.message(Command('inn'))
async def get_inn(message:Message,state:FSMContext):
    await message.answer('Введите ИНН организации :')
    await state.set_state(Inn.inn_text)

@router.message(Inn.inn_text)
async def search_inn(message:Message,state:FSMContext):
    inn_text = message.text.strip()
    link = f'https://dazor.by/search?lang=by&search={inn_text}'
    response = requests.get(link, headers=headers)
    html_content = response.content
    soup = BeautifulSoup(html_content, 'html.parser')

    # Поиск элементов
    text_inn_find = soup.find('dl', class_='mb-0')

    # Обработка первого элемента
    if text_inn_find is None:
        text_inn_find = 'Не найдено.Введите ИНН коректно'
    else:
        text_inn_find = text_inn_find.text.strip()

    lines = text_inn_find.split('\n')

    # Ищем строку с "Код МНС:"
    result_lines = []
    for i in range(len(lines)):
        if lines[i].strip() == "Код МНС:":
            # Объединяем текущую строку и следующую строку (с 435)
            if i + 1 < len(lines):
                combined_line = lines[i].strip() + " " + lines[i + 1].strip()
                result_lines.append(combined_line)
                # Пропускаем следующую строку, так как мы её уже использовали
                # Здесь нужно быть осторожным, чтобы не пропускать другие строки
            else:
                result_lines.append(lines[i].strip())
        elif i > 0 and lines[i - 1].strip() == "Код МНС:":
            # Эта строка уже обработана как часть предыдущей
            continue
        else:
            result_lines.append(lines[i].strip())

    # Выводим результат
    text_inn_find = '\n'.join(result_lines)

    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='🔴 Сайт',url=link)]
    ])
    await message.reply(f'<b>Поиск  🤖💻📱 прошел успешно:</b>\n\n├ ИНН : <a href="https://dazor.by/search?lang=by&search={inn_text}">{inn_text}</a>\n├ Основные данные :\n\n<i>{text_inn_find}</i>',parse_mode='HTML',reply_markup=keyboard)
    await state.clear()

@router.message(Command('add_admin'))
async def add_admin(message:Message,state:FSMContext):
    if message.from_user.id == ADMIN_ID:
       await message.answer('🔃 Введите ID админа которого хотите добавить:')
       await state.set_state(Admin.admin_id)
       return
    else:
        await message.answer('❌ Вы не имеете доступа к этой команде')
        return

@router.message(Admin.admin_id)
async def adding_admin(message:Message,state:FSMContext):
    try:
        admin_id = int(message.text.strip())

        # Проверка корректности ID
        if admin_id <= 0:
            await message.answer('❌ ID должен быть положительным числом')
            await state.clear()
            return

        # Проверка, если ID уже в списке админов
        if admin_id in admin_list:
            await message.answer('⚠️ Этот ID уже есть в списке администраторов')
            await state.clear()
            return


        admin_list.append(admin_id)
        await message.answer(f'✅ ID {admin_id} успешно добавлен в список администраторов.')


    except ValueError:
        await message.answer('❌ Пожалуйста, введите корректный числовой ID')
    finally:
        await state.clear()

@router.message(F.text.startswith('@'))
async def user_osint(message: Message):
    username = message.text.strip()
    not_start = username.replace('@', '')
    if len(username) <= 2:
        await message.answer('Введите коректный username', reply_markup=start_mes)
    else:
        url_for_user = f'https://t.me/{not_start}'

        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text='Telegram', url=url_for_user)]
        ])

        await message.answer(f'Пользователь найден:\nUsername : {username}', reply_markup=keyboard)








