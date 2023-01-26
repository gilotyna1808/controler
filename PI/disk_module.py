import psutil
import time
from threading import Thread, Condition

class disk_check:

    def __init__(self, condition:Condition, start:bool=False):
        self.SLEEP = 1
        #
        self.space_less_than_50 = 0
        self.space_less_than_10 = 0
        self.condition = condition
        if start:
            Thread(target=self.check_disk_space, daemon=True).start()
    
    def check_disk_space(self):
        # i = 40#TODO
        while True:
            last_50,last_10 = (self.space_less_than_50,self.space_less_than_10)
            free_space = 100 - psutil.disk_usage("/").percent
            # free_space = 100 - i#TODO
            # i+=1#TODO
            if free_space < 10: self.space_less_than_10 = 1
            else: self.space_less_than_10 = 0
            if free_space < 50: self.space_less_than_50 = 1
            else: self.space_less_than_50 = 0
            if last_50 != self.space_less_than_50 or last_10 != self.space_less_than_10:
                print(f"### disk_module")
                with self.condition:
                    self.condition.notify()
            time.sleep(self.SLEEP)
    
    def get_if_space_less_50(self):
        return self.space_less_than_50
    
    def get_if_space_less_10(self):
        return self.space_less_than_10
    