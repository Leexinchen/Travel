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


    def remind(self):
        distance_list = [
            self.left_tof_thread.min_distance,
            self.center_tof_thread.min_distance,
            self.right_tof_thread.min_distance
            ]
        min_distance = min(distance_list)
        min_direction = list.index(min_distance)
        play_file = self.calculate_direction(min_direction,self.tof_list[min_direction].min_index)
        os.system('play '+play_file)

    def calculate_direction(self,direction,index):
        direction_str = ['30', '60', '90', '120', '150']
        diff = [-1,0,0,1]
        # TODO 添加距离
        distance = None
        play_file_name = direction_str[direction+1+diff[index]] + '度'+direction+'米'
        return play_file_name






