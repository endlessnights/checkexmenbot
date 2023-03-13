import locale
import re
import sqlite3
import time
from datetime import date, datetime

import telebot
from telebot import types

import config

api_token = '6265665879:AAHAzxt1__rg7jksAMi36VSwsVY3Vb0JiT0'  # test bot @checkextestbot
# api_token = ''  # production bot
bot = telebot.TeleBot(api_token)
users = []
# Connect to the database
conn = sqlite3.connect('kzscamcheckbot.db')
c = conn.cursor()
# Create a table to store user information
c.execute(config.scammers)
conn.commit()
# Create a table to store Group information
c.execute(config.creategroupstable)
conn.commit()
conn.close()