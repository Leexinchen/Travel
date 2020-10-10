
from gps import GPS
from remind import remind_thread

if __name__ == '__main__':
    # 启动GPS
    GPS_thread = GPS()
    GPS_thread.start()
    # 启动提示预警
    remind_thread = remind_thread()
    remind_thread.start()
    # 启动RGB灯带
