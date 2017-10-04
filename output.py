# -*- coding: utf-8 -*-
from __future__ import unicode_literals
def file_parametres(path,data):
	with open(path + '/info.dat', 'w') as out:
		if 'name_result' in data: 
			name = 'Номер расчета в базе'
			text = '{}: {};'.format(name, data['name_result'])
			out.write(text)
			out.write('\n')
			del data['name_result']
		if 'schem' in data:
			name = 'Схема расчета дифракии'
			text = '{}: {};'.format(name, data['schem'])
			out.write(text)
			out.write('\n')
			del data['schem']
		if 'scan' in data: 
			name = 'Тип сканирования'
			text = '{}: {};'.format(name, data['scan'])
			out.write(text)
			out.write('\n')
			del data['scan']
		if 'apparatnaya' in data: 
			name = 'Алгоритм расчета аппаратной функции'
			text = '{}: {};'.format(name, data['apparatnaya'])
			out.write(text)
			out.write('\n')
			del data['apparatnaya']
		if 'computer_calculate' in data: 
			name = 'Вычислительный компьютер'
			text = '{}: {};'.format(name, data['computer_calculate'])
			out.write(text)
			out.write('\n')
			del data['computer_calculate']
		if 'id_comment_calc' in data: 
			name = 'Комментарий к расчету'
			text = '{}: {};'.format(name, data['id_comment_calc'])
			out.write(text)
			out.write('\n')
			del data['id_comment_calc']
		if 'logarifm_scale' in data: 
			name = 'Результат представлен в логарифмической шкале?'
			text = '{} - {};'.format(name, data['logarifm_scale'])
			out.write(text)
			out.write('\n')
			del data['logarifm_scale']



		if 'teta_end' in data:
			name = 'Верхний предел по тета (отстройка по Брегу)'
			text = '{}: {};'.format(name, data['teta_end'])
			out.write(text)
			out.write('\n')
			del data['teta_end']
		if 'teta_start' in data:
			name = 'Нижний предел по тета (отстройка по Брегу)'
			text = '{}: {};'.format(name, data['teta_start'])
			out.write(text)
			out.write('\n')
			del data['teta_start']
		if 'step_shag_teta' in data: 
			name = 'Шаг угла поворота кристалла-образца(тета)'
			text = '{}: {} угл.сек;'.format(name, data['step_shag_teta'])
			out.write(text)
			out.write('\n')
			del data['step_shag_teta']
		if 'anod1' in data: 
			name = 'ka1'
			text = '{}: {} А;'.format(name, data['anod1'])
			out.write(text)
			out.write('\n')
			del data['anod1']
		if 'anod2' in data: 
			name = 'ka2'
			text = '{}: {} А;'.format(name, data['anod2'])
			out.write(text)
			out.write('\n')
			del data['anod2']
		if 'step_lambda' in data: 
			name = 'Шаг по длине волны (спектр источника)'
			text = '{}: {} отн.ед.;'.format(name, data['step_lambda'])
			out.write(text)
			out.write('\n')
			del data['step_lambda']
		if 'step_teta' in data: 
			name = 'Шаг по углу (расходимость источника)'
			text = '{}: {} отн.ед.;'.format(name, data['step_teta'])
			out.write(text)
			out.write('\n')
			del data['step_teta']
		if 'source_divergence_mmetr' in data: 
			name = 'Размер пятна источника'
			text = '{}: {} мм;'.format(name, data['source_divergence_mmetr'])
			out.write(text)
			out.write('\n')
			del data['source_divergence_mmetr']
		if 'source_divergence_arc' in data: 
			name = 'Угловая расходимость источника'
			text = '{}: {} угл. сек.;'.format(name, data['source_divergence_arc'])
			out.write(text)
			out.write('\n')
			del data['source_divergence_arc']



		if ('X0_1' in data) or ('Xh_1' in data) or ('bragg_1' in data):
			out.write('\n')
			out.write('-----кристалл 1-----')
			out.write('\n')
		if 'X0_1' in data: 
			name = 'Х0 (поляризуемость) для 1 кристалла'
			text = '{}: {};'.format(name, data['X0_1'])
			out.write(text)
			out.write('\n')
			del data['X0_1']
		if 'Xh_1' in data: 
			name = 'Хh (поляризуемость) для 1 кристалла'
			text = '{}: {};'.format(name, data['Xh_1'])
			out.write(text)
			out.write('\n')
			del data['Xh_1']
		if ('h1' in data) and ('k1' in data) and ('k1' in data):
			name = 'индексы Миллера hkl'
			text = '{}: {}{}{};'.format(name, data['h1'], data['k1'], data['l1'])
			out.write(text)
			out.write('\n')
			del data['h1']
			del data['k1']
			del data['l1']
		if ('h_surface1' in data) and ('k_surface1' in data) and ('l_surface1' in data):
			name = 'индексы Миллера поверхности hkl'
			text = '{}: {}{}{};'.format(name, data['h_surface1'], data['k_surface1'], data['l_surface1'])
			out.write(text)
			out.write('\n')
			del data['h_surface1']
			del data['k_surface1']
			del data['l_surface1']
		if 'bragg_1' in data: 
			name = 'Угол Брэгга'
			text = '{}: {};'.format(name, data['bragg_1'])
			out.write(text)
			out.write('\n')
			del data['bragg_1']
		if 'fi_1' in data: 
			name = 'угол ассиметрии'
			text = '{}: {} угл.сек.;'.format(name, data['fi_1'])
			out.write(text)
			out.write('\n')
			del data['fi_1']
		if ('X0_2' in data) or ('Xh_2' in data) or ('bragg_2' in data):
			out.write('\n')
			out.write('-----кристалл 2-----')
			out.write('\n')
		if 'X0_2' in data: 
			name = 'Х0 (поляризуемость) для 2 кристалла'
			text = '{}: {};'.format(name, data['X0_2'])
			out.write(text)
			out.write('\n')
			del data['X0_2']
		if 'Xh_2' in data: 
			name = 'Хh (поляризуемость) для 2 кристалла'
			text = '{}: {};'.format(name, data['Xh_2'])
			out.write(text)
			out.write('\n')
			del data['Xh_2']
		if ('h2' in data) and ('k2' in data) and ('k2' in data):
			name = 'индексы Миллера hkl'
			text = '{}: {}{}{};'.format(name, data['h2'], data['k2'], data['l2'])
			out.write(text)
			out.write('\n')
			del data['h2']
			del data['k2']
			del data['l2']
		if ('h_surface2' in data) and ('k_surface2' in data) and ('l_surface2' in data):
			name = 'индексы Миллера поверхности hkl'
			text = '{}: {}{}{};'.format(name, data['h_surface2'], data['k_surface2'], data['l_surface2'])
			out.write(text)
			out.write('\n')
			del data['h_surface2']
			del data['k_surface2']
			del data['l_surface2']
		if 'bragg_2' in data: 
			name = 'Угол Брэгга'
			text = '{}: {};'.format(name, data['bragg_2'])
			out.write(text)
			out.write('\n')
			del data['bragg_2']
		if 'fi_2' in data: 
			name = 'угол ассиметрии'
			text = '{}: {} угл.сек.;'.format(name, data['fi_2'])
			out.write(text)
			out.write('\n')
			del data['fi_2']

		if ('X0_3' in data) or ('Xh_3' in data) or ('bragg_3' in data):
			out.write('\n')
			out.write('-----кристалл 3-----')
			out.write('\n')
		if 'X0_3' in data: 
			name = 'Х0 (поляризуемость) для 3 кристалла'
			text = '{}: {};'.format(name, data['X0_3'])
			out.write(text)
			out.write('\n')
			del data['X0_3']
		if 'Xh_3' in data: 
			name = 'Хh (поляризуемость) для 3 кристалла'
			text = '{}: {};'.format(name, data['Xh_3'])
			out.write(text)
			out.write('\n')
			del data['Xh_3']
		if ('h3' in data) and ('k3' in data) and ('k3' in data):
			name = 'индексы Миллера hkl'
			text = '{}: {}{}{};'.format(name, data['h3'], data['k3'], data['l3'])
			out.write(text)
			out.write('\n')
			del data['h3']
			del data['k3']
			del data['l3']
		if ('h_surface3' in data) and ('k_surface3' in data) and ('l_surface3' in data):
			name = 'индексы Миллера поверхности hkl'
			text = '{}: {}{}{};'.format(name, data['h_surface3'], data['k_surface3'], data['l_surface3'])
			out.write(text)
			out.write('\n')
			del data['h_surface3']
			del data['k_surface3']
			del data['l_surface3']
		if 'bragg_3' in data: 
			name = 'Угол Брэгга'
			text = '{}: {};'.format(name, data['bragg_3'])
			out.write(text)
			out.write('\n')
			del data['bragg_3']
		if 'fi_3' in data: 
			name = 'угол ассиметрии'
			text = '{}: {} угл.сек.;'.format(name, data['fi_3'])
			out.write(text)
			out.write('\n')
			del data['fi_3']


		if 'input_l_slit1' in data: 
			out.write('\n')
			out.write('----щель №1-----')
			out.write('\n')
			name = 'Расстояние от источника до 1 щели'
			text = '{}: {};'.format(name, data['input_l_slit1'])
			out.write(text)
			out.write('\n')
			del data['input_l_slit1']
		if 'input_size_slit1' in data: 
			name = 'Размер 1 щели'
			text = '{}: {} мм.;'.format(name, data['input_size_slit1'])
			out.write(text)
			out.write('\n')
			del data['input_size_slit1']

		if 'input_l_slit2' in data: 
			out.write('\n')
			out.write('----щель №2-----')
			out.write('\n')
			name = 'Расстояние от источника до 2 щели'
			text = '{}: {};'.format(name, data['input_l_slit2'])
			out.write(text)
			out.write('\n')
			del data['input_l_slit2']
		if 'input_size_slit2' in data: 
			name = 'Размер 2 щели'
			text = '{}: {} мм.;'.format(name, data['input_size_slit2'])
			out.write(text)
			out.write('\n')
			del data['input_size_slit2']

		out.write('\n')
		out.write('----Остальные параметры----')
		out.write('\n')	
		for i in data:
			text = '{}: {};'.format(i, data[i])
			out.write(text)
			out.write('\n')
	return True