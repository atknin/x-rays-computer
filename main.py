# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import sys, math, cmath, os, re, scipy # re - для работы с регулярными выражениями
import numpy as np
import matplotlib
from scipy import integrate
from PIL import Image # для выввода изображения
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import matplotlib as mpl

#QDesktopWidget предоставляет информацию о компьютере пользователя
#QMainWindow - создает статус бар
import time
from numpy import random

plt.style.use('ggplot')

from matplotlib import cm
from matplotlib.ticker import LinearLocator, FormatStrFormatter
from numpy  import array
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.utils import COMMASPACE, formatdate
from email import encoders

from matplotlib import animation
from matplotlib import cm
from matplotlib.ticker import LinearLocator, FormatStrFormatter
from numpy  import array
import matplotlib.colors as colors
from PIL import Image, ImageSequence
import imageio
# import psutil
import csv
import zero_crystal
import random, string



class compute:
	def __init__(self, cumpute_dict):
		self.cumpute_dict = cumpute_dict
		self.cumpute_dict['name_result'] = self.randomword(10)

	def randomword(self, length):
		valid_letters='ABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890'
		return ''.join((random.choice(valid_letters) for i in range(length)))
		
	def get_scheme(self):
		if self.cumpute_dict['schem'] == 'zero_crystal':
			return 'Схема: "прямой пучок"'
		else:
			return 'Схема: неизвестная для расчета'

	def start(self):
		if self.cumpute_dict['schem'] == 'zero_crystal':
			zero_crystal.do_it(self.cumpute_dict)
			return 1
		else:
			return 1

		
