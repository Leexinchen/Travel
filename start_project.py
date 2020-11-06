
from gps import GPS
from remind import remind_thread
import remind
from RGB import RGB

def start():
    # 启动GPS
    GPS_thread = GPS()
    GPS_thread.start()
    # 启动提示预警
    remind_thread = remind.remind_thread()
    remind_thread.start()


if __name__ == '__main__':
    start()