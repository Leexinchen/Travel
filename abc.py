
# -*- coding: utf-8-*-
from robot.sdk.AbstractPlugin import AbstractPlugin
import time
import serial

class Plugin(AbstractPlugin):

    def send(self,str):
        self.ser.write(str.encode())

    def handle(self, text, parsed):
        self.ser = serial.Serial("/dev/ttyAMA0", 115200, timeout=1)
        time.sleep(1)
        print(self.ser.read(self.ser.inWaiting()).decode())
        print('init ready.')
        self.send('ATD13588841901;\r')

    def isValid(self, text, parsed):
        return "打电话给紧急联系人" in text