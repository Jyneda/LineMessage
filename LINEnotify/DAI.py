import time, requests
import csmapi, DAN, LINE_notify as LINE 
import config

ServerURL = config.ServerURL 
Reg_addr = None #if None, Reg_addr = MAC address

DAN.profile['dm_name']= 'LineNotify'
DAN.profile['df_list']= ['Msg-O']
DAN.profile['d_name']= config.device_name 

DAN.device_registration_with_retry(ServerURL, Reg_addr)

while True:
    try:
        msg = DAN.pull('Msg-O')   
        if msg:
            print(msg[0])
            LINE.notify(msg[0])
 
    except Exception as e:
        print(e)
        if str(e).find('mac_addr not found:') != -1:
            print('Reg_addr is not found. Try to re-register...')
            DAN.device_registration_with_retry(ServerURL, Reg_addr)
        else:
            print('Connection failed due to unknow reasons.')
            time.sleep(1)    

    time.sleep(config.polling_cycle)

