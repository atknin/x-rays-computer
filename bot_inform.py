# -*- coding: utf-8 -*-
from __future__ import unicode_literals
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import telebot
def sent_to_atknin_bot(message,b):
	chat_id_d= 299006631#dima
	chat_id_v = 180380877#vanya
	chat_id_n = 279568215#Nikita
	
	token = '285455287:AAERVWhSH53FLL1zWERx_u7f7pJJMMP97qA'
	bot = telebot.TeleBot(token)
	if b == "d":
		bot.send_message(chat_id_d, message)
	elif b == "v":
		bot.send_message(chat_id_v, message)
	elif b == "n":
		bot.send_message(chat_id_n, message)
	else:
		bot.send_message(chat_id_d, message)
		bot.send_message(chat_id_v, message)