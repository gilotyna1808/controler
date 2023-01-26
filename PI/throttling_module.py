import subprocess
import time
from threading import Thread, Condition

class throttling_check:

    def __init__(self, condition:Condition, start:bool=False):
        self.SLEEP = 1
        #
        self.current_under_voltage = False
        self.occurred_under_voltage = False
        self.occurred_throttling = False
        self.current_throttling = False
        self.condition = condition
        if start:
            Thread(target=self.check_temperature, daemon=True).start()
    
    def check_temperature(self):
        while True:
            res = self._get_throttling_values()
            if res is not None:
                current_under_voltage = res[0]
                current_throttling = res[1]
                occurred_under_voltage = res[2]
                occurred_throttling = res[3]
            if (current_under_voltage != self.current_under_voltage or 
                current_throttling != self.current_throttling or
                occurred_throttling != self.occurred_throttling or 
                occurred_under_voltage != self.occurred_under_voltage):
                print(f"### throtling_modules")
                self.current_under_voltage = res[0]
                self.current_throttling = res[1]
                self.occurred_under_voltage = res[2]
                self.occurred_throttling = res[3]
                with self.condition:
                    self.condition.notify()
            time.sleep(self.SLEEP)
    
    def _get_throttling_values(self):
        err, msg = subprocess.getstatusoutput('vcgencmd get_throttled')
        if not err:
            msg = bin(int(msg.split("=")[1], 16))[2:]
            msg = msg[::-1]
            c_under_voltage = False
            o_under_voltage = False
            c_throttling = False
            o_throttling = False
            if len(msg) > 0:
                c_under_voltage = msg[0]
            if len(msg) >= 2:
                c_throttling = msg[2]
            if len(msg) >= 16:
                o_under_voltage = msg[16]
            if len(msg) >= 18:
                o_throttling = msg[18]
            return (c_under_voltage,c_throttling,o_under_voltage,o_throttling)

    def get_if_current_under_voltage(self):
        if self.current_under_voltage: return 1
        else: return 0

    def get_if_current_throttling(self):
        if self.current_throttling: return 1
        else: return 0

    def get_if_occurred_under_voltage(self):
        if self.occurred_under_voltage: return 1
        else: return 0

    def get_if_occurred_throttling(self):
        if self.occurred_throttling: return 1
        else: return 0
