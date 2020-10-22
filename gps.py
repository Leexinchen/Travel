import serial
import time
import configs
import threading
from my_print import my_print

class GPS(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.thread_name = 'GPS'
        self.ser = serial.Serial("/dev/ttyAMA0", 115200, timeout=1)
        self.ser.write('AT+GPS=1\r'.encode())
        time.sleep(0.2)
        self.send('AT+CGATT=1\r')
        time.sleep(0.2)
        self.send('AT+CGDCONT=1,"IP","CMNET"\r')
        time.sleep(0.2)
        self.send('AT+CGACT=1,1\r')
        time.sleep(1)
        self.ser.read(self.ser.inWaiting()).decode()
        # my_print(self,self.ser.read(self.ser.inWaiting()).decode())
        # print('[GPS] - ',self.ser.read(self.ser.inWaiting()).decode())
        my_print(self,'init ready.')
        # print('[GPS] - init ready.')

    def run(self) -> None:
        self.get_location()

    def send(self, str):
        self.ser.write(str.encode())

    def read_location(self):
        line_data = self.ser.readline().decode()
        line_head = line_data.split(',')[0]
        location = None
        if len(line_data) is not 0 and (line_head == "$GNRMC"):
            location = line_data
        return location

    def update_location(self, location_N, location_E):
        url = configs.LOCATION_HOST_URL + '?latitude=' + str(location_N) + '&longitude=' + str(location_E)
        s = 'AT+HTTPGET=\"%s\"\r' % url
        # print(s)
        self.send(s)

    def get_location(self):
        self.send('AT+GPSRD=5\r')
        location = None
        while True:
            while True:
                location = self.read_location()
                if location is not None:
                    break
            latitude = location.split(',')[3]
            longitude = location.split(',')[5]
            # 伟度小数部分
            la_mm = float(latitude[2:-1]) / 60
            lo_mm = float(longitude[3:-1]) / 60
            new_latitude = float(latitude[0:2]) + la_mm
            new_longitude = float(longitude[0:3]) + lo_mm
            my_print(self,new_latitude, new_longitude)
            self.update_location(new_latitude, new_longitude)
            my_print(self,'Update success!')
            time.sleep(20)


if __name__ == '__main__':
    UART_func_class = GPS()
    UART_func_class.get_location()
