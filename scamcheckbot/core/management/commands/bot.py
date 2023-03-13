from django.core.management.base import BaseCommand
from telebot import TeleBot
from .secretdata import telegrambotapikey
from .config import starttext, showfounddata
from ...models import Profiles, Scammers, Scammersdata
from django.db.models import Q
from datetime import date, datetime
import locale

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
    fktels = ''
    fktgs = ''
    fkcards = ''
    user_input = message.text
    checkdata = Scammersdata.objects.filter(Q(card=user_input) | Q(tel=user_input) | Q(tg=user_input)).first()
    if checkdata:
        fkdata = Scammersdata.objects.filter(scammer__id=checkdata.scammer.id)
        for data in fkdata:
            fktels += f"{data.tel}\n"
            fktgs += f"{data.tg}\n"
            fkcards += f"{data.card}\n"
        locale.setlocale(locale.LC_TIME, 'ru_RU.UTF-8')
        scammeradded = datetime.strptime(str(checkdata.scammer.added), '%Y-%m-%d')
        scammeradded = datetime.strftime(scammeradded, '%d %B %Y')
        bot.send_message(message.chat.id, text=showfounddata.format(checkdata.scammer.name, checkdata.scammer.taxid, scammeradded, checkdata.scammer.fraudcount,
           checkdata.scammer.fraudsum, checkdata.scammer.comment, fktels, fktgs, fkcards))
    else:
        bot.send_message(message.chat.id, text='Совпадений не найдено')


class Command(BaseCommand):
    help = 'Implemented to Django application telegram bot setup command'

    def handle(self, *args, **kwargs):
        bot.enable_save_next_step_handlers(delay=2)  # Сохранение обработчиков
        bot.load_next_step_handlers()  # Загрузка обработчиков
        bot.polling(none_stop=True)
