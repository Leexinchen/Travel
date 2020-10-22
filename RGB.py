import threading

from rpi_ws281x import Adafruit_NeoPixel, Color

import configs
from my_print import my_print


class RGB(threading.Thread):

    def __init__(self):
        threading.Thread.__init__(self)
        self.thread_name = "RGB_LIGHT"
        my_print(self,'init done!')


    def run(self) -> None:
        self.do_lighting()

    def do_lighting(self):

        strip = Adafruit_NeoPixel(configs.LED_COUNT, configs.LED_PIN, configs.LED_FREQ_HZ, configs.LED_DMA, configs.LED_INVERT, configs.LED_BRIGHTNESS)

        strip.begin()

        for i in range(0, strip.numPixels()):
            strip.setPixelColor(i, Color(255, 255, 0))

        strip.show()

if __name__ == '__main__':
    th = RGB()
    th.start()