from django.core.management.base import BaseCommand
from telebot import TeleBot
from .secretdata import telegrambotapikey
from .config import starttext, showfounddata
from ...models import Profiles, Scammers, Scammersdata
from django.db.models import Q
from datetime import date, datetime
import locale
from django.db.models import F

bot = TeleBot(telegrambotapikey, threaded=False)


@bot.message_handler(commands=['start'])
def hellouser(message):
    p, _ = Profiles.objects.get_or_create(
        userid=message.chat.id,
        defaults={
            'username': message.from_user.username,
        }
    )
    bot.send_message(message.chat.id, text=starttext.format(p.username))


@bot.message_handler(content_types=['text'])
def text_message(message):
    p, _ = Profiles.objects.get_or_create(
        userid=message.chat.id,
        defaults={
            'username': message.from_user.username,
        }
    )
    fktels = ''
    fktgs = ''
    fkcards = ''
    user_input = message.text
    if user_input[0] == '8':
        user_input = '7' + user_input[1:]
    user_input = (user_input.replace(" ", "")).replace("+", "")
    checkdata = Scammersdata.objects.filter(Q(card=user_input) | Q(tel=user_input) | Q(tg=user_input)).first()
    if checkdata:
        obj = Scammers.objects.get(id=checkdata.scammer.id)
        obj.checkcount = F('checkcount') + 1
        obj.save()
        fkdata = Scammersdata.objects.filter(scammer__id=checkdata.scammer.id)

        for data in fkdata:
            if data.tel:
                fcelnum = data.tel
                fcelnum = '+' + format(int(fcelnum[:-1]), ",").replace(",", " ") + fcelnum[-1]
                fktels += f"{fcelnum}\n"
            if data.tg:
                fktgs += f"{data.tg}\n"
            if data.card:
                fkcard = f"{data.card[0:4]} {data.card[4:8]} {data.card[8:12]} {data.card[12:16]}"
                fkcards += f"{fkcard}\n"
        locale.setlocale(locale.LC_TIME, 'ru_RU.UTF-8')
        scammeradded = datetime.strptime(str(checkdata.scammer.added), '%Y-%m-%d')
        scammeradded = datetime.strftime(scammeradded, '%d %B %Y')
        bot.send_message(message.chat.id,
                         text=showfounddata.format(checkdata.scammer.name,
                                                   checkdata.scammer.taxid,
                                                   scammeradded,
                                                   checkdata.scammer.fraudcount,
                                                   checkdata.scammer.fraudsum,
                                                   checkdata.scammer.comment,
                                                   fktels, fktgs, fkcards,
                                                   checkdata.scammer.checkcount
                                                   ))
    else:
        bot.send_message(message.chat.id, text='Совпадений не найдено')


class Command(BaseCommand):
    help = 'Implemented to Django application telegram bot setup command'

    def handle(self, *args, **kwargs):
        bot.enable_save_next_step_handlers(delay=2)  # Сохранение обработчиков
        bot.load_next_step_handlers()  # Загрузка обработчиков
        bot.polling(none_stop=True)
