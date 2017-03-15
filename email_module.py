# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import smtplib
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.base import MIMEBase
from email.utils import COMMASPACE, formatdate
from email import encoders
# from email.header import Header
from bot_inform import sent_to_atknin_bot
from computer import *


def notification(message):
    try:
        sent_to_atknin_bot(comp_name + ' ' + message,"n")
        sent_to_atknin_bot(comp_name + ' ' + message,"v")
    except Exception as e:
        print(comp_name + message+' (bad telegram)')

def sendEmail(msge,email):
	me = 'info@crys.ras.ru'
	you = email
	msg = MIMEMultipart('alternative')
	msg['Subject'] = u"Ваш Результат: "+ msge['title']
	msg['From'] = me
	msg['To'] = you
	htmlmsgtext = """<h2>Расчет окончен</h2>
                <p>\
                 """ + msge['text'] + """\
                 </p>
                <p><strong>Имеется два вложения</strong></p><br />"""
# добавляем анимацию
	body = MIMEMultipart('alternative')
	body.attach(MIMEText(msge['text']))
	body.attach(MIMEText(htmlmsgtext, 'html'))
	msg.attach(body)
	try:
		with open(msge['gif'],'rb') as fil:
			part2 = MIMEImage(fil.read(),name = os.path.basename(msge['gif']))
			msg.attach(part2)
			print('gif вложен в письмо')

	except Exception as e:
		print(e)
# добавляем тектовые файлы
	try:
		for fff in msge['dat']:
			with open(fff,'rb') as fil:
				part3 = MIMEBase('application', "octet-stream")
				part3.set_payload( fil.read() )
				encoders.encode_base64(part3)
				part3.add_header('Content-Disposition', 'attachment; filename="{0}"'.format(os.path.basename(fff)))
				msg.attach(part3)
				print('dat вложен в письмо')
	except Exception as e:
		print(e)

	s = smtplib.SMTP('mail.crys.ras.ru', 25)
	#s.starttls()
	s.login('info','62syHMgV')
	s.sendmail(me, you, msg.as_string())
	print('письмо отправлено')
	s.quit()
