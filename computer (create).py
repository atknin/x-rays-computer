comp = 3
comp_name = '313 КАГ компьютер: '

def notification(message):
    try:
        sent_to_atknin_bot(comp_name + message,"n")
        sent_to_atknin_bot(comp_name + message),"v")
    except Exception as e:
        print(comp_name + message+' (bad telegram)')
