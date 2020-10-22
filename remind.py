import time

from distance import tof_thread
import threading
import os
import configs
from my_print import my_print


class remind_thread(threading.Thread):

    def __init__(self):
        threading.Thread.__init__(self)
        self.thread_name = 'REMIND'
        self.left_tof_thread = tof_thread(configs.TOF_LEFT_BUS, 'LEFT_SENSOR')
        self.center_tof_thread = tof_thread(configs.TOF_CENTER_BUS, 'CENTER_SENSOR')
        self.right_tof_thread = tof_thread(configs.TOF_RIGHT_BUS, 'RIGHT_SENSOR')
        self.tof_list = [
            self.left_tof_thread,
            self.center_tof_thread,
            self.right_tof_thread
            ]
        # self.bottom_tof_thread = tof_thread(configs.TOF_BOTTOM_BUS, 'bottom')

    def run(self) -> None:
        self.left_tof_thread.start()
        self.center_tof_thread.start()
        self.right_tof_thread.start()
        # self.bottom_tof_thread.start()
        time.sleep(3)
        while True:
            left_dis = self.left_tof_thread.min_distance
            center_dis = self.center_tof_thread.min_distance
            right_dis = self.right_tof_thread.min_distance
            my_print(self,left_dis,center_dis,right_dis)
            my_print(self,'--------------------------')
            if left_dis <configs.REMIND_DISTANCE or center_dis <configs.REMIND_DISTANCE or right_dis <configs.REMIND_DISTANCE:
                self.remind()
                time.sleep(1)
            # time.sleep(0.5)


    def remind(self):
        distance_list = [
            self.left_tof_thread.min_distance,
            self.center_tof_thread.min_distance,
            self.right_tof_thread.min_distance
            ]
        min_distance = min(distance_list)
        min_direction = distance_list.index(min_distance)
        play_file = self.calculate_direction(min_direction,self.tof_list[min_direction].min_index,min_distance)
        # os.system('play '+play_file)

    def get_min_dis(self,distance):
        #得到文件名最低的语音
        dis = configs.DISTANCE_STR[-1]
        for i in range(1,configs.DISTANCE_STR.__len__()-1):
            if distance >= configs.DISTANCE_STR[i-1] and distance <= configs.DISTANCE_STR[i]:
                dis = configs.DISTANCE_STR[i]
        return  dis


    def calculate_direction(self,direction,index,distance):
        direction_str = ['左前方60度', '左前方30度', '正前方90度', '右前方30度', '右前方60度']
        diff = [-1, -1, 0, 0]
        distance = self.get_min_dis(distance)
        direction_index = 2
        # 左右方向求索引
        if direction != 1:
            direction_index = int((direction/2))*3+1+diff[index]
        # play_file_name = configs.FILE_BASE_PATH + direction_str[direction+1+diff[index]] +str(distance)+'米有障碍物.wav'
        play_file_name = configs.FILE_BASE_PATH + direction_str[direction_index] +str(distance)+'米有障碍物.wav'
        my_print(self,play_file_name)
        return play_file_name

if __name__ == '__main__':
    remind_thread = remind_thread()
    remind_thread.start()


