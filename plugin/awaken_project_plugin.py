import os
from robot.sdk.AbstractPlugin import AbstractPlugin

class Plugin(AbstractPlugin):

    def handle(self, text, parsed):
        self.say('已经在启动啦!', cache=True)
        os.system('python3 ~/Travel-1/start_project.py')
        os.system('sudo python3 ~/Travel-1/RGB.py')
        self.say('启动完成，放心地出门吧!', cache=True)

    def isValid(self, text, parsed):
        return "我要出行" in text