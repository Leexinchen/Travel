import serial
import time
class UART_func():

    def __init__(self):
        self.ser=serial.Serial("/dev/ttyAMA0",115200,timeout=1)
        time.sleep(1)
        print(self.ser.read(self.ser.inWaiting()).decode())
        print('init ready.')

    def send(self,str):
        self.ser.write(str.encode())

    def call(self):
        self.send('ATD13588841901;\r')

if __name__ == '__main__':
    UART_func_class = UART_func()
    UART_func_class.call()
        # time.sleep(20)