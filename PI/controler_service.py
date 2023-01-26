import pi_device_message_module as pi
import mag_module as mag
from threading import Condition, Thread
from datetime import datetime
con = Condition()
con2 = Condition()

message = pi.raspberry_message(con,True)
mag_message = mag.magnetometr_check(con2,True)

def temp(con):
    while 1: 
        with con:
            now = datetime.now()
            m =message.get_message()
            # print(f"[CONTROL SERVICE PI] {now.hour}:{now.minute}:{now.second}.{now.microsecond}")
            print(f"{m} BIN:{bin(int(m.split(',')[1][:-3]))}")
            con.wait()        

def aaa(con):
   while 1: 
        with con:
            now = datetime.now()
            # print(f"[CONTROL SERVICE MAG] {now.hour}:{now.minute}:{now.second}.{now.microsecond}")
            m =mag_message.get_message()
            print(f"{m} BIN:{bin(int(m.split(',')[1][:-3]))}")
            con.wait()        

Thread(target=temp, args=(con,)).start()
Thread(target=aaa, args=(con2,)).start()