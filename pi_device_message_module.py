import time
from disk_module import disk_check
from measuring_module import measuring_check
from program_module import program_check
from temperature_module import temperature_check
from throttling_module import throttling_check
from threading import Thread,Condition
from datetime import datetime

class raspberry_message():

    def __init__(self, start:bool=False):
        #
        self.condition = Condition()
        self.message_condition = Condition()
        #
        self.disk_module = disk_check(self.message_condition,True)
        self.measuring_module = measuring_check("/home/srr/GEO-OPR-2/Geometrics-Opr/data/",self.message_condition,True)
        self.program_module = program_check("/tmp/geometrics_rasp.pid", self.message_condition, True)
        self.temperature_module = temperature_check(self.message_condition, True)
        self.throttling_module = throttling_check(self.message_condition,True)
        #
        self.message = "$PRPI0000000000000000*00"
        if start:
            Thread(target=self.update_message,daemon=True).start()
    
    def update_message(self):
        while True:
            with self.message_condition:
                self.message = self.create_message()
                self.message_condition.wait(1)
                with self.condition: self.condition.notify()

    def get_condition(self):
        return self.condition

    def create_message(self):
        message = "00"
        message += f"{self.disk_module.get_if_space_less_10()}"
        message += f"{self.throttling_module.get_if_current_under_voltage()}"
        message += f"{self.throttling_module.get_if_current_throttling()}"
        message += f"{self.temperature_module.get_if_temperature_more_80()}"
        message += f"{self.measuring_module.get_if_measurement_is_working()}"
        message += f"{self.program_module.get_if_program_is_working()}"
        message += f"0000"
        message += f"{self.disk_module.get_if_space_less_50()}"
        message += f"{self.temperature_module.get_if_temperature_more_50()}"
        message += f"{self.throttling_module.get_if_occurred_under_voltage()}"
        message += f"{self.throttling_module.get_if_occurred_throttling()}"
        message = str(int(message,2))
        # message = "{:02x}".format(message).upper()
        check_sum = self.get_checksum(message)
        # now = datetime.now()
        # print(f"[CREATE MESSAGE] {now.hour}:{now.minute}:{now.second}.{now.microsecond}")
        return f"$PPI,{message}*{check_sum}".upper()


    def get_checksum(self, message):
        checksum = 0
        for el in message:
            checksum ^= ord(el)
        return "{:02x}".format(checksum)
    
    def get_message(self):
        return self.message
    
# condition_change = Condition()
# disk_m = disk_check(condition_change,True)
# mes_m = measuring_check("lol",condition_change,True)
# program_m = program_check("/tmp/geometrics_rasp.pid", condition_change, True)
# temperature_m = temperature_check(condition_change, True)
# throttling_m = throttling_check(condition_change,True)
# while 1:
#     with condition_change:
#         now = datetime.now()
#         now = f"[{now.hour}:{now.minute}:{now.second}.{now.microsecond}]"
#         print(f'{now}\nDisk < 10:{disk_m.get_if_space_less_10()}\nDisk < 50:{disk_m.get_if_space_less_50()}')
#         print(f'Temp > 50:{temperature_m.get_if_temperature_more_50()}\nTemp > 80:{temperature_m.get_if_temperature_more_80()}')
#         print(f"Is working: {mes_m.get_if_measurement_is_working()}")
#         print(f"Is program working: {program_m.get_if_program_is_working()}")
#         print(f"C UV{throttling_m.get_if_current_under_voltage()}")
#         print(f"C T{throttling_m.get_if_current_throttling()}")
#         print(f"O UV{throttling_m.get_if_occurred_under_voltage()}")
#         print(f"O T{throttling_m.get_if_occurred_throttling()}")
#         condition_change.wait(2)