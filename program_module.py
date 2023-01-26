import os
import time
import psutil
from threading import Thread, Condition

class program_check:

    def __init__(self, path:str, condition:Condition, start:bool=False):
        self.SLEEP = 1
        #
        self.pid_file_path = path
        self.program_is_working = False
        self.condition = condition
        if start:
            Thread(target=self.check_program, daemon=True).start()
    
    def check_program(self):
        while True:
            is_working = self._get_if_pid_exist()
            if is_working != self.program_is_working:
                print(f"### program_module")
                self.program_is_working = is_working
                with self.condition:
                    self.condition.notify()            
            time.sleep(self.SLEEP)
    
    def _get_if_pid_exist(self):
        if os.path.exists(self.pid_file_path):
            try:
                with open(self.pid_file_path, "r") as f:
                    pid = f.readline()
                    if psutil.pid_exists(int(pid)):
                        return True
            except:pass
        return False
    
    def get_if_program_is_working(self):
        if self.program_is_working: return 0
        return 1    