import os
import time
from threading import Thread, Condition

class measuring_check:

    def __init__(self, path:str, condition:Condition, start:bool=False):
        self.SLEEP = 1
        #
        self.dir_path = path
        self.last_dir_size = 0
        self.measurement_is_working = False
        self.condition = condition
        if start:
            Thread(target=self.check_measurement, daemon=True).start()
    
    def check_measurement(self):
        while True:
            current_dir_size = self._get_dir_size()
            is_working = current_dir_size > self.last_dir_size
            self.last_dir_size = current_dir_size
            if is_working != self.measurement_is_working:
                print(f"### mesurment_module")
                self.measurement_is_working = is_working
                with self.condition:
                    self.condition.notify()            
            time.sleep(self.SLEEP)
    
    def _get_dir_size(self):
        size = 0
        for file in os.scandir(self.dir_path):
            size += os.path.getsize(file)
        return size

    def get_if_measurement_is_working(self):
        if self.measurement_is_working: return 0
        return 1