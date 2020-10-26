import time

from RGB import RGB
from distance import tof_thread
import threading
import os
import configs
from my_print import my_print


class remind_thread(threading.Thread):

    def __init__(self):
        threading.Thread.__init__(self)
        self.thread_name = 'REMIND'
        # 启动RGB灯带
        # self.RGB_thread = RGB()
        # self.RGB_thread.start()

        self.left_tof_thread = tof_thread(configs.TOF_LEFT_BUS, 'LEFT_SENSOR')
        self.center_tof_thread = tof_thread(configs.TOF_CENTER_BUS, 'CENTER_SENSOR')
        self.right_tof_thread = tof_thread(configs.TOF_RIGHT_BUS, 'RIGHT_SENSOR')
        self.tof_list = [
            self.left_tof_thread,
            self.center_tof_thread,
            self.right_tof_thread
            ]
        self.bottom_tof_thread = tof_thread(configs.TOF_BOTTOM_BUS, 'BOTTOM_SENSOR')

    def run(self) -> None:
        self.left_tof_thread.start()
        self.center_tof_thread.start()
        self.right_tof_thread.start()
        self.bottom_tof_thread.start()
        time.sleep(3)
        while True:
            remind_type =  self.bottom_remind()
            # self.RGB_thread.remind_type = remind_type
            if remind_type is not True:
                remind_type = self.remind()
                # self.RGB_thread.remind_type = remind_type
            else:
                time.sleep(1)
            time.sleep(1)
            # time.sleep(0.5)

    def bottom_remind(self):
        bottom_distance = self.bottom_tof_thread.get_distance()
        if bottom_distance < configs.BOTTOM_REMIND_DISTANCE:
            my_print(self,'bottom '+ str(bottom_distance))
            distance = self.get_min_dis(bottom_distance,bottom=True)
            # 播放提示
            play_file = configs.FILE_BASE_PATH+'正前方90度路面'+str(distance)+'米有障碍物.wav'
            os.system('play '+play_file+' &')
            return True
        return False

    def remind(self):
        left_dis = self.left_tof_thread.min_distance
        center_dis = self.center_tof_thread.min_distance
        right_dis = self.right_tof_thread.min_distance
        my_print(self, left_dis, center_dis, right_dis)
        my_print(self, '--------------------------')
        if left_dis < configs.REMIND_DISTANCE or center_dis < configs.REMIND_DISTANCE or right_dis < configs.REMIND_DISTANCE:
            distance_list = [
                left_dis,
                center_dis,
                right_dis
                ]
            min_distance = min(distance_list)
            min_direction = distance_list.index(min_distance)
            play_file = self.calculate_direction(min_direction,self.tof_list[min_direction].min_index,min_distance)
            os.system('play '+play_file+' &')
            return True
        return False

    def get_min_dis(self,distance,bottom=False):
        dis_list = configs.DISTANCE_STR
        if bottom:
            dis_list = configs.BOTTOM_DISTANCE_STR
        #得到文件名最低的语音
        dis = dis_list[-1]
        for i in range(1,dis_list.__len__()-1):
            if distance >= dis_list[i-1] and distance <= dis_list[i]:
                dis = dis_list[i]
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


