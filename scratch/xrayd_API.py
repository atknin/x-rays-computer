a = "{'anod2': '0.713590', 'source_divergence_mmetr': '0.5', 'logarifm_scale': 'log', 'step_teta': '1', 'step_lambda': '1', 'id_email': 'atknini@yandex.ru', 'id_comment_calc': '%s', 'anod1': '0.709300', 'id_source': '7', 'teta_end': '10', 'Xh_1': '12.0462 + 0.1358j', 'step_shag_teta': '0.2', 'Xh_2': '6.8599 + 0.6087j', 'schem': 'double_crystal_light', 'bragg_1': '21.6785', 'input_size_slit2': '0.02', 'computer_calculate': '', 'X0_2': '-72.3175 + 3.5266j', 'input_l_slit1': '0.57', 'bragg_2': '%s', 'scan': '2theta', 'X0_1': '-31.7799 + 0.1558j', 'fi_1': '0', 'apparatnaya': 'our', 'teta_start': '-10', 'input_size_slit1': '0.02', 'fi_2': '0', 'input_l_slit2': '1.005', 'source_divergence_arc': '600'}"
import requests

with open('/Users/Atknini/Desktop/new.dat','w') as f:
    i = 19.0

    while True:
        if i > 24:
            break
        i+=0.1
        r = requests.post('http://x-rays.world/diffraction/api/', data = {'data':a% ('result_'+str(round(i,2)).replace('.','_'), str(round(i,2))),'id_email':'atknini@yandex.ru','computer_calculate':'SKB313'})
        print(round(i,2))
