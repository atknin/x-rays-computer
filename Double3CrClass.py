# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import math
from functions import *
import email_module
import json

class double():
    def __init__(self, input_data):
        self.data = {}

        self.data['scan']               =    str(input_data['scan'])
        self.data['path']               =    str(input_data['path']) + '/'
        self.data['wavelength_1']       =    float(input_data['anod1'])                          * 1e-10
        self.data['wavelength_2']       =    float(input_data['anod2'])                          * 1e-10
        self.data['sigma']              =    float(input_data['source_divergence_arc'])
        self.data['S1']                 =    float(input_data['input_size_slit1'])               * 1e-3
        self.data['S2']                 =    float(input_data['input_size_slit2'])               * 1e-3
        self.data['L1x']                =    float(input_data['input_l_slit1'])       
        self.data['L2x']                =    float(input_data['input_l_slit2'])
        self.data['X0_1']               =    complex(input_data['X0_1'])                         * 1e-7
        self.data['Xh_1']               =    complex(input_data['Xh_1'])                         * 1e-7
        self.data['X0_2']               =    complex(input_data['X0_2'])                         * 1e-7
        self.data['Xh_2']               =    complex(input_data['Xh_2'])                         * 1e-7
        self.data['bragg_1']            =    float(input_data['bragg_1'])
        self.data['bragg_2']            =    float(input_data['bragg_2'])
        self.data['fi_monohrom']        =    float(input_data['fi_1'])
        self.data['fi_sample']          =    float(input_data['fi_2'])
        self.data['name_result']        =    str(input_data['name_result'])
        self.data['id_comment_calc']    =    str(input_data['id_comment_calc'])
        self.data['id_email']           =    str(input_data['id_email'])
        self.data['slits']              = [ -math.degrees(math.atan(self.data['S2'] /2/self.data['L2x']))* 3600, \
                                             math.degrees(math.atan(self.data['S2'] /2/self.data['L2x']))* 3600, \
                                            -math.degrees(math.atan(self.data['S1'] /2/self.data['L1x']))* 3600, \
                                             math.degrees(math.atan(self.data['S1'] /2/self.data['L1x']))* 3600  ]
        self.data['surf_plot_x_lim']    = [  float(input_data['teta_start']),                           \
                                             float(input_data['teta_end'])]
        self.data['sigma_metr']         =    float(input_data['source_divergence_mmetr'])       * 1e-3

        self.data['svertka_plot_x_lim'] = [  float(input_data['teta_start']),                           \
                                             float(input_data['teta_end'])] 
        self.data['shag_itta']          =    float(input_data['step_lambda']) *     math.radians(5/3600)
        
        self.data['itta_1']             =    0.996  # предел интегрирования от
        self.data['itta_2']             =    1.01  # предел интегрирования до
        self.data['shag_teta']          =    float(input_data['step_teta'])/8 *    math.radians(float(1/3600))

        self.data['dTeta']              =    math.radians(self.data['surf_plot_x_lim'][0]       /3600)
        self.data['dTeta_end']          =    math.radians(self.data['surf_plot_x_lim'][1]       /3600)
        self.data['dTeta_shag']         =    math.radians(float(input_data['step_shag_teta'])   /3600)

        #Определяем тип источника /ss - синхротрон, иначе трубка
        if  ('type_source' in input_data) and (input_data['type_source'] == 'ss'):
            print('[.] источник СИ')
            self.data['wavelength_1']  =  float(input_data['anod'])                            * 0.8
            self.data['wavelength_1']  =  float(input_data['anod'])                            * 1.2
            self.g_lambd = ss_lambd 
        else:
            print('[.] лабораторный источник')
            self.g_lambd = ls_lambd

        #Определяем тип монохроматора / double_crystal - двухкристальный монохроматор
        if  ('type_monochromator' in input_data) and (input_data['type_monochromator'] == 'double_crystal'):
            print('[.] двухкристальный монохроматор')
            self.monohromator_curve = doubelCr_monohromator_curve
        else:
            self.monohromator_curve = singlelCr_monohromator_curve
            print('[.] однокристальный монохроматор')
        print('[.] параметры инизиализировны - двухкристальный эксперимент')

    def start(self):
        email_module.notification(" Старт: " + self.data['id_comment_calc'])
        self.file_write_normirovka = open(self.data['path'] + self.data['name_result'] + '_normirovka.dat', 'w')
        self.file_write = open(self.data['path'] + self.data['name_result'] + '.dat', 'w')
        if self.data['scan'] == '2theta':
            self.DoubleTheta()
        else:
            self.Omega()
        self.file_write.close()
        self.file_write_normirovka.close()
        email_module.notification('Расчет окончен для '+self.data['id_email'])
    
    def UpdateProgresWeb(self,prcents):
        try:
            payload = {'progress':self.data['name_result'],'value':int(prcents)}
            req_f = get_request('http://62.109.0.242/diffraction/compute/',payload)
            string = req_f.read().decode('utf-8')
            req_son_obj = json.loads(string)
            if req_son_obj['typeof'] == 1:
                return True
                print('[.расчет остановлен]')
            else:
                return False
        except Exception as e:
            print('ошибка обновления прогресс бара: ',e)
            return False

    def DoubleTheta(self):
        dTeta = dTeta_st =  self.data['dTeta']
        dTeta_shag = self.data['dTeta_shag']
        dTeta_end = self.data['dTeta_end']
        itta_1 = self.data['itta_1']
        itta_2 = self.data['itta_2']
        shag_itta = self.data['shag_itta']
        shag_teta = self.data['shag_teta']
        wavelength_1 = self.data['wavelength_1']
        wavelength_2 = self.data['wavelength_2']
        L1x = self.data['L1x']
        L2x = self.data['L2x']
        S1 = self.data['S1']
        S2 = self.data['S2']
        sigma_metr = self.data['sigma_metr']
        X0_1 = self.data['X0_1']
        Xh_1 = self.data['Xh_1']
        X0_2 = self.data['X0_2']
        Xh_2 = self.data['Xh_2']
        bragg_1 = self.data['bragg_1']
        bragg_2 =self.data['bragg_2']
        fi_sample = self.data['fi_sample'] 
        fi_monohrom = self.data['fi_monohrom']

        sdvigka = 0
        i = 0
        tet = teta_lims(0,L1x,L2x,S1,S2,sigma_metr)
        # 1-------------------------------------------------------------------------------------------------------------------
        while dTeta <= dTeta_end:
            # Обновляем прогресс бар
            prcents = (dTeta-dTeta_st+dTeta_shag) / (dTeta_end - dTeta_st)*100
            if self.UpdateProgresWeb(prcents):
                return False
            cli_progress_test(prcents)

            itta = itta_1
            # 2-----------------------------------------------------------------------------------------------------------
            P = 0
            normirovka = 0
            while itta <= itta_2:
                teta = tet[0]
                func_lambda = self.g_lambd(itta, wavelength_1, wavelength_2)
                # 3-----------------------------------------------------------------------------------------------------------
                while teta <= tet[1]:
                    without_sample = func_lambda*slit_extensive_source(math.degrees(teta)*3600,sdvigka,L1x,L2x,S1,S2,sigma_metr)*self.monohromator_curve(teta, itta, X0_1, Xh_1, bragg_1, fi_monohrom)
                    P += without_sample*sample_curve(dTeta, teta, itta, X0_2, Xh_2, bragg_2, fi_sample)*sample_curve(math.radians(sdvigka)/3600, teta, itta, X0_1, Xh_1, bragg_1, fi_monohrom)
                    normirovka += without_sample 
                    teta += shag_teta
                #----3-----------------------------------------------------
                itta += shag_itta
            #-2----------------------------------------------------------------
            self.file_write.write('%14.8f' % (math.degrees(dTeta)*3600))
            self.file_write_normirovka.write('%14.8f' % (math.degrees(dTeta)*3600))
            try:
                P /= normirovka
            except ZeroDivisionError:
                P = 0
            self.file_write.write('%14.8f' %  (P))
            self.file_write_normirovka.write('%14.8f' %  (normirovka))
            self.file_write.write('\n')
            self.file_write_normirovka.write('\n')
            i += 1
            dTeta += dTeta_shag
        # 1-------------------------------------------------------------------------------------------------------------------
        return True

    def Omega(self):
        dTeta = dTeta_st = self.data['dTeta']
        dTeta_shag = self.data['dTeta_shag']
        dTeta_end = self.data['dTeta_end']
        itta_1 = self.data['itta_1']
        itta_2 = self.data['itta_2']
        shag_itta = self.data['shag_itta']
        shag_teta = self.data['shag_teta']
        wavelength_1 = self.data['wavelength_1']
        wavelength_2 = self.data['wavelength_2']
        L1x = self.data['L1x']
        L2x = self.data['L2x']
        S1 = self.data['S1']
        S2 = self.data['S2']
        sigma_metr = self.data['sigma_metr']
        X0_1 = self.data['X0_1']
        Xh_1 = self.data['Xh_1']
        X0_2 = self.data['X0_2']
        Xh_2 = self.data['Xh_2']
        bragg_1 = self.data['bragg_1']
        bragg_2 =self.data['bragg_2']
        fi_sample = self.data['fi_sample']
        fi_monohrom = self.data['fi_monohrom']

        i = 0

        # 1-------------------------------------------------------------------------------------------------------------------
        while dTeta <= dTeta_end:
            # Обновляем прогресс бар
            prcents = (dTeta-dTeta_st+dTeta_shag) / (dTeta_end - dTeta_st)*100
            
            self.UpdateProgresWeb(prcents)
            cli_progress_test(prcents)

            itta = itta_1
            sdvigka = -2*(math.degrees(dTeta)*3600)
            # определяем пределы интегрирования по тета
            tet = teta_lims(sdvigka,L1x,L2x,S1,S2,sigma_metr)
            #----2-------------------------------------------------------------
            P = 0
            normirovka = 0
            while itta <= itta_2:
                teta = tet[0] #- 2*dTeta  #второй знак
                func_lambda = self.g_lambd(itta, wavelength_1, wavelength_2)
                #----3-----------------------------------------------------
                while teta <= tet[1]:
                    without_sample = func_lambda*slit_extensive_source(math.degrees(teta)*3600,sdvigka,L1x,L2x,S1,S2,sigma_metr)*self.monohromator_curve(teta, itta, X0_1, Xh_1, bragg_1, fi_monohrom)
                    P += without_sample*sample_curve(dTeta, teta, itta, X0_2, Xh_2, bragg_2, fi_sample)*sample_curve(math.radians(sdvigka)/3600, teta, itta, X0_1, Xh_1, bragg_1, fi_monohrom)
                    normirovka += without_sample  
                    teta += shag_teta
                    #----/3------------------------------------------------
                itta += shag_itta
            #/2----------------------------------------------------------------

            self.file_write.write('%14.8f' % (math.degrees(dTeta)*3600))
            self.file_write_normirovka.write('%14.8f' % (math.degrees(dTeta)*3600))
            try:
                P /= normirovka
            except ZeroDivisionError:
                P = 0
            self.file_write.write('%14.8f' %  (P))
            self.file_write_normirovka.write('%14.8f' %  (normirovka))
            self.file_write.write('\n')
            self.file_write_normirovka.write('\n')
            i += 1
            dTeta += dTeta_shag
        #/1--------------------------------------------------------------------
        return True
