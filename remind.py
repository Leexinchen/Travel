import time

from distance import tof_thread
import threading
import os
import configs

class remind_thread(threading.Thread):

    def __init__(self):
        threading.Thread.__init__(self)
        self.left_tof_thread = tof_thread(configs.TOF_LEFT_BUS, 'left')
        self.center_tof_thread = tof_thread(configs.TOF_CENTER_BUS, 'center')
        self.right_tof_thread = tof_thread(configs.TOF_RIGHT_BUS, 'right')
        self.tof_list = [
            self.left_tof_thread,
            self.center_tof_thread,
            self.right_tof_thread
            ]
        self.bottom_tof_thread = tof_thread(configs.TOF_BOTTOM_BUS, 'bottom')

    def run(self) -> None:
        self.left_tof_thread.start()
        self.center_tof_thread.start()
        self.right_tof_thread.start()
        self.bottom_tof_thread.start()
        while True:
            if self.left_tof_thread.min_distance<configs.REMIND_DISTANCE or self.center_tof_thread.min_distance<configs.REMIND_DISTANCE or self.right_tof_thread.min_distance<configs.REMIND_DISTANCE:
                self.remind()
            # time.sleep(0.5)


    def remind(self):
        distance_list = [
            self.left_tof_thread.min_distance,
            self.center_tof_thread.min_distance,
            self.right_tof_thread.min_distance
            ]
        min_distance = min(distance_list)
        min_direction = list.index(min_distance)
        play_file = self.calculate_direction(min_direction,self.tof_list[min_direction].min_index,min_distance)
        os.system('play '+play_file)

    def get_min_dis(self,distance):
        #得到文件名最低的语音
        for i in range(0,configs.DISTANCE_STR.__len__()-1):
            if distance >= configs.DISTANCE_STR[i] and distance <= configs.DISTANCE_STR[i+1]:
                return configs.DISTANCE_STR[i]
        return  configs.DISTANCE_STR[-1]


    def calculate_direction(self,direction,index,distance):
        direction_str = ['左前方60度', '左前方30度', '正前方90度', '右前方30度', '右前方60度']
        diff = [-1,0,0,1]
        # T
        distance = self.get_min_dis(distance)
        play_file_name = direction_str[direction+1+diff[index]] +distance+'米有障碍物.wav'
        return play_file_name






