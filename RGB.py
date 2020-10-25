import threading
import time

from rpi_ws281x import Adafruit_NeoPixel, Color

import configs
from my_print import my_print


class RGB(threading.Thread):

    def __init__(self):
        threading.Thread.__init__(self)
        self.thread_name = "RGB_LIGHT"
        self.strip = Adafruit_NeoPixel(configs.LED_COUNT, configs.LED_PIN, configs.LED_FREQ_HZ, configs.LED_DMA, configs.LED_INVERT, configs.LED_BRIGHTNESS)
        self.strip.begin()
        init_color = Color(0,0,0)
        self.led_colors = [init_color for i in range(configs.LED_COUNT)]
        # 预警返回值,如果为1，则需要颜色预警
        self.remind_type = 0
        my_print(self,'init done!')


    def run(self) -> None:
        while True:
            if self.remind_type:
                # 先清除颜色
                self.colorWipe(Color(0,0,0),0)
                self.breath_chase()
                self.remind_type=0
            self.rainbowCycle()

    #功能一-逐个变色-
    # colorWipe(self.strip, Color(255, 0, 0))  # Red wipe
    # 所有灯逐个变成红色
    def colorWipe(self,color, wait_ms=50):
        """Wipe color across display a pixel at a time."""
        for i in range(self.strip.numPixels()):
            self.strip.setPixelColor(i, color)
            self.strip.show()
            time.sleep(wait_ms/1000.0)

    # 呼吸闪烁
    def  breath_chase(self,wait_ms = 10):
        for i in range(0,255,3):
            now_color = Color(i,0,0)
            # 所有灯珠设置一遍
            self.colorWipe(now_color,0)
            # 延时
            time.sleep(wait_ms/1000.0)
        for i in range(255,0,-3):
            now_color = Color(i,0,0)
            self.colorWipe(now_color,0)
            time.sleep(wait_ms/1000.0)

    # 渐变至某个颜色
    def gradient_change(self,color):
        pass

    # 白色交替闪烁
    def theaterChase(self, color, wait_ms=50, iterations=10):
        """Movie theater light style chaser animation."""
        for j in range(iterations):
            for q in range(3):
                for i in range(0, self.strip.numPixels(), 3):
                    self.strip.setPixelColor(i+q, color)
                self.strip.show()
                time.sleep(wait_ms/1000.0)
                for i in range(0, self.strip.numPixels(), 3):
                    self.strip.setPixelColor(i+q, 0)

    # 支撑函数
    def wheel(self,pos):
        """Generate rainbow colors across 0-255 positions."""
        if pos < 85:
            return Color(pos * 3, 255 - pos * 3, 0)
        elif pos < 170:
            pos -= 85
            return Color(255 - pos * 3, 0, pos * 3)
        else:
            pos -= 170
            return Color(0, pos * 3, 255 - pos * 3)

    #功能三-彩虹色整体统一柔和渐变-每个灯颜色同一时间相同
    def rainbow(self, wait_ms=20, iterations=1):
        """Draw rainbow that fades across all pixels at once."""
        for j in range(256*iterations):
            for i in range(self.strip.numPixels()):
                self.strip.setPixelColor(i, self.wheel((i+j) & 255))
            self.strip.show()
            time.sleep(wait_ms/1000.0)


    #功能四-彩虹色每一个灯各自柔和渐变-每个灯颜色同一时间不同
    def rainbowCycle(self, wait_ms=20, iterations=5):
        """Draw rainbow that uniformly distributes itself across all pixels."""
        for j in range(256*iterations):
            # 如果颜色渐变的时候预警了，推出循环
            if self.remind_type == 1:
                break
            for i in range(self.strip.numPixels()):
                self.strip.setPixelColor(i, self.wheel((int(i * 256 / self.strip.numPixels()) + j) & 255))
            self.strip.show()
            time.sleep(wait_ms/1000.0)


    #功能五-彩虹色统一闪烁流动变色-每个灯颜色同一时间相同
    def theaterChaseRainbow(self,wait_ms=50):
        """Rainbow movie theater light style chaser animation."""
        for j in range(256):
            for q in range(3):
                for i in range(0, self.strip.numPixels(), 3):
                    self.strip.setPixelColor(i+q, self.wheel((i+j) % 255))
                self.strip.show()
                time.sleep(wait_ms/1000.0)
                for i in range(0, self.strip.numPixels(), 3):
                    self.strip.setPixelColor(i+q, 0)

    def test(self):
        print ('Color wipe animations.')
        self.colorWipe( Color(155, 0, 0))  # Red wipe
        self.colorWipe( Color(0, 255, 0))  # Blue wipe
        self.colorWipe( Color(0, 0, 255))  # Green wipe
        print ('Theater chase animations.')
        self.theaterChase( Color(127, 127, 127))  # White theater chase
        self.theaterChase( Color(127,   0,   0))  # Red theater chase
        self.theaterChase(Color(  0,   0, 127))  # Blue theater chase
        print ('Rainbow animations.')
        self.rainbow()
        self.rainbowCycle()
        self.theaterChaseRainbow()

if __name__ == '__main__':
    th = RGB()
    th.start()
