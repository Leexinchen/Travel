import time
import sys
import signal
import VL53L1X
import threading

from my_print import my_print


class tof_thread(threading.Thread):
    def __init__(self,thread_id,thread_name):
        threading.Thread.__init__(self)
        self.min_index = 0
        self.min_distance = 10000
        self.thread_id = thread_id
        self.thread_name = thread_name
        # sensor init
        self.tof = VL53L1X.VL53L1X(i2c_bus=thread_id, i2c_address=0x29)
        self.tof.open()
        self.tof.start_ranging(3)
        self.tof.set_timing(20, 25)
        # time.sleep(5)


    def run(self):
        my_print(self,self.thread_name + 'sensor start!')
        while True:
            self.min_index, self.min_distance = self.get_distance()
            # print(self.thread_name,self.min_index, self.min_distance)

    def get_distance(self):
        min_index = 0
        min_distance = 10000
        for i in range(0, 4):
            row_list = list()
            for j in range(0, 4):
                left_x = j * 3
                right_x = j * 3 + 3
                bot_y = i * 3
                top_y = i * 3 + 3
                roi = VL53L1X.VL53L1xUserRoi(left_x, right_x, bot_y, top_y)
                self.tof.set_user_roi(roi)
                distance = self.tof.get_distance()
                row_list.append(distance)
                # print("距离障碍物"+str(distance)+"cm远")
            row_min = min(row_list)
            if min_distance > row_min:
                min_distance = row_min
                min_index = row_list.index(row_min)
        return min_index,min_distance/1000

    def __del__(self):
        self.tof.stop_ranging()

if __name__ == '__main__':
    thread3 = tof_thread(4, 'sensor_3')
    thread2 = tof_thread(3, 'sensor_2')
    thread1 = tof_thread(1, 'sensor_1')

    thread1.start()
    thread2.start()
    thread3.start()