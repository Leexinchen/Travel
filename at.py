import serial
import time
import configs

class UART_func():

    def __init__(self):
        self.ser=serial.Serial("/dev/ttyAMA0",115200,timeout=1)
        self.ser.write('AT+GPS=1\r'.encode())
        time.sleep(0.2)
        self.send('AT+CGATT=1\r')
        time.sleep(0.2)
        self.send('AT+CGDCONT=1,"IP","CMNET"\r')
        time.sleep(0.2)
        self.send('AT+CGACT=1,1\r')
        time.sleep(1)
        print(self.ser.read(self.ser.inWaiting()).decode())
        print('init ready.')

    def send(self,str):
        self.ser.write(str.encode())

    def read_location(self):
        line_data = self.ser.readline().decode()
        print(line_data)
        # data_list = data.split('\r\n')
        location = None

        if len(line_data) is not 0 and (line_data[0] == '2' or line_data[0] == '3'):
            location = line_data
            # break
        print(location)
        return location

    def call(self):
        self.send('ATD13588841901;\r')

    def update_location(self, location_N,location_E):
        url = configs.LOCATION_HOST_URL+'?latitude='+str(location_N)+'&longitude='+str(location_E)
        s = 'AT+HTTPGET=\"%s\"\r'%url
        print(s)
        self.send(s)

        while True:
            line = self.ser.readline().decode()
            # print(line)
            #判断响应头
            if line == '+HTTPRECV:HTTP/1.1 200 OK\r\n':
                break
        # print('-------ssss')
        # 手动清缓存
        while True:
            line = self.ser.readline().decode()
            #print(line)
            if line == '}':
                break
        # self.read()

    def get_location(self):
        self.send('AT+LOCATION=2\r')
        location = None
        while True:
            location = self.read_location()
            # print('location',location)
            if location is not None:
                break
        latitude = location.split(',')[0]
        longitude = location.split(',')[1][:-2]
        #伟度小数部分
        la_mm = float(latitude[2:-1])/60
        lo_mm = float(longitude[3:-1])/60
        new_latitude = float(latitude[0:2])+la_mm
        new_longitude = float(longitude[0:3])+lo_mm
        print(new_latitude,new_longitude)
        self.update_location(new_latitude,new_longitude)
        print('#Update success!')
        time.sleep(10)
        # self.ser.read(self.ser.inWaiting())
        # self.ser.flushInput()

if __name__ == '__main__':
    UART_func_class = UART_func()
    UART_func_class.get_location()
        # time.sleep(20)