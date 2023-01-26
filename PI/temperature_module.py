import time
import psutil
from threading import Thread, Condition

class temperature_check:

    def __init__(self, condition:Condition, start:bool=False):
        self.SLEEP = 1
        #
        self.temperature_more_than_80 = 0
        self.temperature_more_than_50 = 0
        self.condition = condition
        if start:
            Thread(target=self.check_temperature, daemon=True).start()
    
    def check_temperature(self):
        while True:
            last_80, last_50 = (self.temperature_more_than_80, self.temperature_more_than_50)
            temperature = psutil.sensors_temperatures()['cpu_thermal'][0][1]
            # temperature = psutil.sensors_temperatures()['coretemp'][0][1]#TODO
            if temperature > 80: self.temperature_more_than_80 = 1
            else: self.temperature_more_than_80 = 0
            if temperature > 50: self.temperature_more_than_50 = 1
            else: self.temperature_more_than_50 = 0
            if last_80 != self.temperature_more_than_80 or last_50 != self.temperature_more_than_50:
                print(f"### temperature_module")
                with self.condition:
                    self.condition.notify()
            time.sleep(self.SLEEP)
    
    def get_if_temperature_more_80(self):
        return self.temperature_more_than_80
    
    def get_if_temperature_more_50(self):
        return self.temperature_more_than_50
    