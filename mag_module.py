import time
import socket
import json
from threading import Thread, Condition

class magnetometr_check():
    def __init__(self, start:bool=False):
        self.conditions = Condition()

        #
        self.message = "$PMG,0000000000000000*00"
        
        if start:
            Thread(target=self.server_mag_data, daemon=True).start()
    
    def server_mag_data(self):
        socket_listener = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        socket_listener.bind(("localhost", 21947))
        while True:
            try:
                data, _ = socket_listener.recvfrom(4096)
                frame = json.loads(data)
                self.message = self.create_message(frame)
                with self.conditions: self.conditions.notify()
            except socket.timeout as ex:
                print(f'[TIMEOUT]')
    
    def get_condition(self):
        return self.conditions

    def create_message(self, frame):
        message  = ""
        message += f"{self._get_critical_fault(frame)}"
        message += f"{self._get_mag_0_critical_fault(frame)}"
        message += f"{self._get_mag_1_critical_fault(frame)}"
        message += f"{self._get_if_board_temp_more_than_65(frame)}"
        message += f"{self._get_if_fgga_temp_more_than_65(frame)}"
        message += f"{self._get_non_critical_fault(frame)}"
        message += f"{self._get_if_board_temp_more_than_50(frame)}"
        message += f"{self._get_if_fgga_temp_more_than_50(frame)}"
        message += f"{self._get_mag_0_valid(frame)}"
        message += f"{self._get_mag_1_valid(frame)}"
        message += f"{self._get_mag_0_heating(frame)}"
        message += f"{self._get_mag_1_heating(frame)}"
        message += f"{self._get_system_status(frame)}"
        message = str(int(message,2))
        # message = "{:02x}".format(message).upper()
        check_sum = self._get_checksum(message)
        return f"$PMG,{message}*{check_sum}".upper()

    def get_message(self):
        return self.message
    
    def _get_checksum(self, message):
        checksum = 0
        for el in message:
            checksum ^= ord(el)
        return "{:02x}".format(checksum)
    
    def _get_mag_0_valid(self, frame):
        value = frame['id']['mag_0_data_valid']
        if value: return 0
        return 1

    def _get_mag_1_valid(self, frame):
        value = frame['id']['mag_1_data_valid']
        if value: return 0
        return 1
    
    def _get_mag_0_heating(self, frame):
        value = frame['mag_0_status']['startup_diagnostic']
        if "Cell_heating" in value: return 1
        return 0

    def _get_mag_1_heating(self, frame):
        value = frame['mag_1_status']['startup_diagnostic']
        if "Cell_heating" in value: return 1
        return 0

    def _get_system_status(self, frame):
        hibernate, magnetometer, calibration, startup = (0,0,0,0)
        value = frame['sys_stat']['running_mode']
        if "Calibration" in value:
            calibration = 1
        if "Magnetometer" in value:
            magnetometer = 1
        if "Startup" in value:
            startup = 1
        if "Hibernate" in value:
            hibernate = 1
        return f"{hibernate}{magnetometer}{calibration}{startup}"

    def _get_if_fgga_temp_more_than_50(self, frame):
        value = 43 + ((frame['aux_word_0']-2568)/10)
        if value > 50:
            return 1
        return 0

    def _get_if_board_temp_more_than_50(self, frame):
        value = 36.6 - ((frame['aux_word_1']-1790)/10)
        if value > 50:
            return 1
        return 0

    def _get_if_fgga_temp_more_than_65(self, frame):
        value = 43 + ((frame['aux_word_0']-2568)/10)
        if value > 65:
            return 1
        return 0

    def _get_if_board_temp_more_than_65(self, frame):
        value = 36.6 - ((frame['aux_word_1']-1790)/10)
        if value > 65:
            return 1
        return 0
    
    def _get_non_critical_fault(self, frame):
        value = frame['sys_stat']['non_critical_fault']
        if value: return 1
        return 0

    def _get_critical_fault(self, frame):
        value = frame['sys_stat']['critical_fault']
        if value: return 1
        return 0

    def _get_mag_0_critical_fault(self, frame):
        value = frame['mag_0_status']['sensor_fault_id']
        if value >= 5: return 1
        return 0

    def _get_mag_1_critical_fault(self, frame):
        value = frame['mag_1_status']['sensor_fault_id']
        if value >= 5: return 1
        return 0