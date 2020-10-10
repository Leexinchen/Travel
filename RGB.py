import threading



class RGB(threading.Thread):

    # TODO 实现方法
    def __init__(self):
        threading.Thread.__init__(self)


    def run(self) -> None:
        self.do_lighting()

    def do_lighting(self):
        pass

